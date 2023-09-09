from flask import Flask, render_template, request, flash
from main import *

app = Flask(__name__)

manager = Manager()


@app.route("/", methods=['POST', 'GET'])
def home():
    title = 'Strona główna'
    manager.load_data()

    nazwa_kupno = request.form.get("nazwa_kupno")
    cena_kupno = request.form.get("cena_kupno")
    liczba_kupno = request.form.get("liczba_kupno")

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
        'show_balance': show_account_balance(),
        'list': show_list_of_products(),
        'purchase': to_purchase(),
        'sale': to_sale(),
        'balance_request': balance_request(),
    }
    return render_template('index.html', context=context)


@app.route("/historia")
def history():
    title = 'Historia'
    context = {
        'title': title,
        'history': show_action_history(),
    }
    return render_template('historia.html', context=context)
