import json
import os

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
def balance_request(number, saldo):
    if number == 1:
        manager.stan_konta += saldo
        akcja = f'Dodano {saldo} $ do konta'
        manager.historia_akcji.append(akcja)
    elif number == 2:
        manager.stan_konta -= saldo
        akcja = f'Odjęto {saldo} $ z konta'
        manager.historia_akcji.append(akcja)
    else:
        return None


# funkcja odpowiadajaca za sprzedaz z magazynu
def to_sale(nazwa_sprzedaz, cena_sprzedaz, liczba_sprzedaz):
    if nazwa_sprzedaz not in manager.stan_magazynu:
        return None
    else:
        laczna_cena = cena_sprzedaz * liczba_sprzedaz
        produkt_do_sprzedazy = manager.stan_magazynu[nazwa_sprzedaz]['ilość']
        if produkt_do_sprzedazy < liczba_sprzedaz:
            return None
        else:
            produkt_do_sprzedazy -= liczba_sprzedaz
            manager.stan_konta += laczna_cena
            manager.stan_magazynu[nazwa_sprzedaz]['ilość'] -= liczba_sprzedaz
            akcja = f'Sprzedano {nazwa_sprzedaz} w ilosci {liczba_sprzedaz} za {laczna_cena} $'
            manager.historia_akcji.append(akcja)


# funkcja odpowiadajaca za zakup produktow na magazyn
def to_purchase(nazwa_kupno, cena_kupno=0, ilosc_kupno=0):
    if nazwa_kupno not in manager.stan_magazynu:
        laczna_cena = cena_kupno * ilosc_kupno
        if laczna_cena > manager.stan_konta:
            return None
        elif laczna_cena < manager.stan_konta:
            manager.stan_magazynu[nazwa_kupno] = {'ilość': ilosc_kupno, 'cena': cena_kupno}
            manager.stan_konta -= laczna_cena
            akcja = f'Zakupiono {nazwa_kupno} w ilosci {ilosc_kupno} za {laczna_cena} $'
            manager.historia_akcji.append(akcja)
    else:
        return None


# funkcja ktora sprawdza stan konta
def show_account_balance():
    return manager.stan_konta


# funkcja wyswietlajaca liste produktow na magazynie
def show_list_of_products():
    for k, v in manager.stan_magazynu.items():
        print(f'{k} : {v}')


# funkcja, ktora odpowiada za przeglad historii zmian
def show_action_history():
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


