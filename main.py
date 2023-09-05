from Manager import manager

# wlasciwa czesc programu
while True:
    print("1.Wpisz 'saldo' aby dodać lub odjąć kwotę z konta"
        "\n2.Wpisz 'sprzedaz' aby wybrać SPRZEDAŻ"
        "\n3.Wpisz 'zakup' aby wybrać ZAKUP"
        "\n4.Wpisz 'konto' aby wyświetlić stan konta"
        "\n5.Wpisz 'lista' aby wyświetlić pełny stan magazynu"
        "\n6.Wpisz 'magazyn' aby wyświetlić ilość konkretnego produktu na stanie"
        "\n7.Wpisz 'przeglad' aby wyświetlić historię zmian"
        "\n8.Wpisz 'koniec' aby zakończyć działanie programu")
    zapytanie = input("Co wybierasz? : ")

# jezeli podanej wartosci nie ma na liscie warunkow program pyta uzytkownika jeszcze raz co chce zrobic
    if zapytanie not in manager.warunki:
        print('Wpisałeś nieprawidłową wartość.Spróbuj jeszcze raz!')

# dodanie i odjecie przez uzytkownika kwoty z konta
    elif zapytanie == 'saldo':
        manager.execute(zapytanie)

# sprzedaz, ktora dodaje kwote wpisana przez uzytkownika do salda i odejmuje dane produkty z magazynu
    elif zapytanie == 'sprzedaz':
        manager.execute(zapytanie)

# zakup, ktory odejmuje kwote z konta i dodaje produkty do magazynu
    elif zapytanie == 'zakup':
        manager.execute(zapytanie)

# podaje stan konta w $
    elif zapytanie == 'konto':
        manager.execute(zapytanie)

# wyswietla wszystkie produkty ich ilosc i cene jakie sa w magazynie
    elif zapytanie == 'lista':
        manager.execute(zapytanie)

# wyswietla tylko jeden produkt podany przez uzytkownika
    elif zapytanie == 'magazyn':
        manager.execute(zapytanie)

# historia dokonanych przez uzytkownika akcji, ktore zapisuja sie na liscie
    elif zapytanie == 'przeglad' and len(manager.historia_akcji) > 0:
        manager.execute(zapytanie)

# Jeżeli użytkownik wpisuje "koniec", program kończy działanie
    elif zapytanie == "koniec":
        manager.save_to_file()
        break


