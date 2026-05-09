from flask import Blueprint, render_template, request
from services.stock_api import fetch_stock
from services.stock_service import (
    save_stock_data,
    get_all_stocks,
    delete_stock,
    update_stock
)

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/fetch/<symbol>')
def fetch(symbol):
    df = fetch_stock(symbol)
    save_stock_data(symbol, df)
    return f"{symbol} data fetched and stored!"
@stock_bp.route('/edit/<int:id>')
def edit(id):
    data = get_all_stocks()
    stock = [row for row in data if row[0] == id][0]
    return render_template("edit.html", stock=stock)

@stock_bp.route('/stocks')
def stocks():
    data = get_all_stocks()
    return render_template("stocks.html", data=data)


@stock_bp.route('/delete/<int:id>')
def delete(id):
    delete_stock(id)
    return "Deleted!"


@stock_bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    value = request.form.get('value')
    update_stock(id, value)
    return "Updated!"