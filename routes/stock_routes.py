from flask import Blueprint
from flask import render_template
import pandas as pd

from services.top_companies import get_top_companies
from ml.forecast import generate_forecast

stock_bp = Blueprint(
    'stock_bp',
    __name__
)


@stock_bp.route('/')
def home():

    return render_template(
        'index.html'
    )


# Top20

@stock_bp.route('/top20')
def top20():

    df = get_top_companies(20)

    data = df.values.tolist()

    return render_template(

        'top_companies.html',

        data=data,

        title='Top 20 Companies'
    )


# Top50

@stock_bp.route('/top50')
def top50():

    df = get_top_companies(50)

    data = df.values.tolist()

    return render_template(

        'top_companies.html',

        data=data,

        title='Top 50 Companies'
    )


# Top100

@stock_bp.route('/top100')
def top100():

    df = get_top_companies(100)

    data = df.values.tolist()

    return render_template(

        'top_companies.html',

        data=data,

        title='Top 100 Companies'
    )


# Summary

@stock_bp.route('/summary')
def summary():

    df = pd.read_csv(
        "output/model_summary.csv"
    )

    data = df.values.tolist()

    return render_template(

        'model_summary.html',

        data=data
    )


# Company

@stock_bp.route('/company/<ticker>')
def company(ticker):

    ticker = ticker.upper()

    generate_forecast(
        ticker
    )

    df = pd.read_csv(

        f"output/forecast_results/{ticker}.csv"

    )

    data = df.values.tolist()

    return render_template(

        'company_forecast.html',

        data=data,

        ticker=ticker
    )