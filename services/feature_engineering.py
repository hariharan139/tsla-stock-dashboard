# import pandas as pd

# def prepare_features(df):

#     df['prev_close'] = df['Adj Close'].shift(1)
#     df['rolling_mean_5'] = df['Adj Close'].rolling(5).mean()

#     df['target'] = df['Adj Close'].shift(-1)

#     df.dropna(inplace=True)

#     return df

def prepare_features(df):
    
    df['pct_change'] = (
        df['Adj Close']
        .pct_change()
        *100
    )

    df['prev_close'] = (
        df['Adj Close']
        .shift(1)
    )

    df['rolling_mean_5'] = (
        df['Adj Close']
        .rolling(5)
        .mean()
    )

    df.dropna(inplace=True)

    return df