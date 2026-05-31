import pandas as pd


def get_top_companies(n):

    df = pd.read_csv(
        "data/stock_score.csv"
    )

    df = df.sort_values(
        by='Mkt Cap(M)',
        ascending=False
    )

    return df.head(n)