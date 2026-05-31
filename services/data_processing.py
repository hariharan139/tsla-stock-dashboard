# import matplotlib
# matplotlib.use('Agg')

# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# def process_data():
#     df = pd.read_csv("data/TSLA.csv")

#     df = df[['Date', 'Adj Close']]
#     df['Date'] = pd.to_datetime(df['Date'])
#     df = df.sort_values('Date')

#     df['pct_change'] = df['Adj Close'].pct_change() * 100

#     df['Month'] = df['Date'].dt.to_period('M')
    
#     monthly = df.groupby('Month')['Adj Close'].agg(['first', 'last']).reset_index()

#     monthly['1monthchange'] = ((monthly['last'] - monthly['first']) / monthly['first']) * 100

#     df = df.merge(monthly[['Month', '1monthchange']], on='Month', how='left')

#     df['is_last'] = df.groupby('Month')['Date'].transform('max') == df['Date']
    
#     df.loc[~df['is_last'], '1monthchange'] = None

#     os.makedirs("output", exist_ok=True)
    
#     df.to_csv("output/processed_TSLA.csv", index=False)

#     return df, monthly


# def create_graph(monthly):
#     last_24 = monthly.tail(24)

#     plt.figure(figsize=(10,5))
#     plt.plot(last_24['Month'].astype(str), last_24['1monthchange'])

#     plt.xticks(rotation=45)
#     plt.xlabel("Month")
#     plt.ylabel("1 Month Change (%)")
#     plt.title("TSLA Monthly Change (Last 2 Years)")

#     plt.tight_layout()
#     plt.savefig("static/graph.png")
#     plt.close()

from services.stock_api import fetch_stock
from services.feature_engineering import prepare_features


def process_stock(ticker):

    df = fetch_stock(ticker)

    df = prepare_features(df)

    return df