# import yfinance as yf
# import pandas as pd

# def fetch_stock(symbol):
#     df = yf.download(symbol, period="1y")

#     # Fix MultiIndex
#     if isinstance(df.columns, pd.MultiIndex):
#         df.columns = df.columns.get_level_values(0)

#     df.reset_index(inplace=True)

#     print("Columns:", df.columns)  # DEBUG

#     # Handle column differences safely
#     if 'Adj Close' in df.columns:
#         price_col = 'Adj Close'
#     elif 'Close' in df.columns:
#         price_col = 'Close'
#     else:
#         raise Exception("No price column found!")

#     df = df[['Date', price_col]]
#     df.rename(columns={price_col: 'Adj Close'}, inplace=True)

#     df['pct_change'] = df['Adj Close'].pct_change() * 100

#     return df

import yfinance as yf
import pandas as pd


def fetch_stock(ticker):

    df = yf.download(
        ticker,
        period="10y",
        auto_adjust=True
    )

    df.reset_index(inplace=True)

    df = df[
        [
            'Date',
            'Close'
        ]
    ]

    df.rename(
        columns={
            'Close':'Adj Close'
        },
        inplace=True
    )

    return df