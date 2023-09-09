from flask import Flask, render_template, request
from main import *

app = Flask(__name__)



@app.route("/", methods=['POST', 'GET'])
def home():
    title = 'Strona główna'
    manager.load_data()

    nazwa_kupno = None
    cena_kupno = None
    liczba_kupno = None
    nazwa_sprzedaz = None
    cena_sprzedaz = None
    liczba_sprzedaz = None

    if request.method == 'POST':
        nazwa_kupno = request.form.get("nazwa_kupno")
        cena_kupno = int(request.form.get("cena_kupno"))
        liczba_kupno = int(request.form.get("liczba_kupno"))

        nazwa_sprzedaz = request.form.get("nazwa_sprzedaz")
        cena_sprzedaz = request.form.get("cena_sprzedaz")
        liczba_sprzedaz = request.form.get("liczba_sprzedaz")

        if nazwa_kupno and cena_kupno and liczba_kupno:
            to_purchase(nazwa_kupno, int(cena_kupno), int(liczba_kupno))

        if nazwa_sprzedaz and cena_sprzedaz and liczba_sprzedaz:
            to_sale(nazwa_sprzedaz, int(cena_sprzedaz), int(liczba_sprzedaz))

        manager.save_to_file()

    context = {
        'title': title,
        'show_balance': show_account_balance,
        'list': show_list_of_products,
        'purchase': to_purchase(nazwa_kupno, cena_kupno, liczba_kupno),
        'sale': to_sale(nazwa_sprzedaz, cena_sprzedaz, liczba_sprzedaz),
        'balance_request': balance_request,
    }
    return render_template('index.html', context=context)


@app.route("/historia")
def history():
    title = 'Historia'
    context = {
        'title' : title,
        'history': show_action_history,
        'load': manager.load_data()
    }
    return render_template('historia.html', context=context)