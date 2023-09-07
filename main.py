from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    title = 'Strona główna'
    context = {
        'title': title,

    }
    return render_template('index.html', context=context)


@app.route("/historia")
def history():
    title = 'Historia'
    return render_template('historia.html', title=title)


# zainicjowanie klasy manager
class Manager:
    def __init__(self):
        self.data = {}
        self.warunki = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
        self.stan_magazynu = dict()
        self.historia_akcji = []
        self.akcja = 0
        self.stan_konta = 1000
        self.filename = 'history.json'
        self.actions = {}

# metoda-dekorator
    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate

# metoda wywolujaca funkcje na podstawie nazwy
    def execute(self, name):
        if name not in self.actions:
            print('Błąd')
        else:
            self.actions[name](self)

# metoda wczytujaca wartosci do obiektu
    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.stan_konta = data.get('stan_konta', 0)
                    self.stan_magazynu = data.get('stan_magazynu', {})
                    self.historia_akcji = data.get('historia_akcji', [])
            except json.JSONDecodeError:
                self.save_to_file()

    # metoda zapisujaca wartosci obiektu do pliku tekstowego
    def save_to_file(self):
        data = {
            'stan_konta': self.stan_konta,
            'stan_magazynu' : self.stan_magazynu,
            'historia_akcji' : self.historia_akcji
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)

# utworzenie instacji klasy Manager, wczytanie historii i wartosci z pliku
manager = Manager()
manager.load_data()


# funkcja dodajaca i odejmujaca kwote z konta
@manager.assign('saldo')
def balance_request(manager):
    while True:
        try:
            zapytanie_o_saldo = int(input('Wybierz 1 jeżeli chcesz dodać kwotę. Wybierz 2 jeżeli chcesz odjąć kwotę: '))
        except ValueError:
            print('Wpisz 1 lub 2')
            continue
        if zapytanie_o_saldo == 1:
            try:
                saldo = float(input('Wpisz kwotę: '))
            except ValueError:
                print('To nie jest prawidłowa liczba')
                continue
            manager.stan_konta += saldo
            print(f'Dodano {saldo} $ do konta')
            akcja = f'Dodano {saldo} $ do konta'
            manager.historia_akcji.append(akcja)
            break
        elif zapytanie_o_saldo == 2:
            try:
                saldo = float(input('Wpisz kwotę: '))
            except ValueError:
                print('To nie jest prawidłowa liczba')
                continue
            manager.stan_konta -= saldo
            print(f'Odjęto {saldo} $ z konta')
            akcja = f'Odjęto {saldo} $ z konta'
            manager.historia_akcji.append(akcja)
            break
        else:
            print('Podano nieprawidłową liczbę')


# funkcja odpowiadajaca za sprzedaz z magazynu
@manager.assign('sprzedaz')
def to_sale(manager):
    nazwa_produktu = input('Podaj jaki produkt ma zostać sprzedany: ')
    if nazwa_produktu not in manager.stan_magazynu:
        print('Nie ma takiego produktu w magazynie!')
    else:
        cena_produktu = float(input('Podaj cenę: '))
        liczba_sztuk = int(input('Podaj ilość: '))
        laczna_cena = cena_produktu * liczba_sztuk
        produkt_do_sprzedazy = manager.stan_magazynu[nazwa_produktu]['ilość']
        if produkt_do_sprzedazy < liczba_sztuk:
            print('Nie ma takiej ilości!')
        else:
            produkt_do_sprzedazy -= liczba_sztuk
            manager.stan_konta += laczna_cena
            manager.stan_magazynu[nazwa_produktu]['ilość'] -= liczba_sztuk
            print(f'Sprzedano {nazwa_produktu} w ilosci {liczba_sztuk} za {laczna_cena} $')
            akcja = f'Sprzedano {nazwa_produktu} w ilosci {liczba_sztuk} za {laczna_cena} $'
            manager.historia_akcji.append(akcja)


# funkcja odpowiadajaca za zakup produktow na magazyn
@manager.assign('zakup')
def to_purchase(manager):
    nazwa_produktu = input('Podaj jaki produkt ma zostać zakupiony: ')
    if nazwa_produktu not in manager.stan_magazynu:
        cena_produktu = float(input('Podaj cenę produktu: '))
        liczba_sztuk = int(input('Podaj liczbę zakupionych sztuk: '))
        laczna_cena = cena_produktu * liczba_sztuk
        if laczna_cena > manager.stan_konta:
            print('Brakuje pieniędzy na zakup')
        elif laczna_cena < manager.stan_konta:
            manager.stan_magazynu[nazwa_produktu] = {'ilość': liczba_sztuk, 'cena': cena_produktu}
            manager.stan_konta -= laczna_cena
            print(f'Zakupiono {nazwa_produktu} w ilosci {liczba_sztuk} za {laczna_cena} $')
            akcja = f'Zakupiono {nazwa_produktu} w ilosci {liczba_sztuk} za {laczna_cena} $'
            manager.historia_akcji.append(akcja)
    else:
        print('Taki produkt znajduje się już na magazynie')


# funkcja ktora sprawdza stan konta
@manager.assign('konto')
def show_account_balance(manager):
    print(f'Stan konta to :{manager.stan_konta} $')


# funkcja wyswietlajaca liste produktow na magazynie
@manager.assign('lista')
def show_list_of_products(manager):
    print('Lista produktów w magazynie:')
    for k, v in manager.stan_magazynu.items():
        print(f'{k} : {v}')


# funkcja, ktora po wywolaniu sprawdza czy i jezeli jest ilosc wpisanego produktu na stanie
@manager.assign('magazyn')
def show_product(manager):
    pytanie = input('Zapas jakiego produktu chcesz zobaczyć?: ')
    if pytanie not in manager.stan_magazynu:
        print('Nie ma takiego produktu w magazynie!')
    else:
        print(f'{pytanie} : {manager.stan_magazynu.get(pytanie)}')


# funkcja, ktora odpowiada za przeglad historii zmian
@manager.assign('przeglad')
def show_action_history(manager):
    while True:
        while True:
            try:
                liczba_od = int(input('Podaj początek zakresu: '))
                liczba_do = int(input('Podaj koniec zakresu: '))
                break
            except ValueError:
                print(manager.historia_akcji)
        if liczba_od <= 0 or liczba_do > len(manager.historia_akcji):
            print(f'Podałeś liczby spoza zakresu. Oto liczba dotychczasowych akcji : {len(manager.historia_akcji)}')
        else:
            print(manager.historia_akcji[liczba_od - 1:liczba_do])
            break


