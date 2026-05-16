import pandas as pd

def prepare_features(df):

    # Create future target
    df['target'] = df['Adj Close'].shift(-1)

    # Features
    df['prev_close'] = df['Adj Close'].shift(1)
    df['rolling_mean_5'] = df['Adj Close'].rolling(5).mean()

    # Drop nulls
    df.dropna(inplace=True)

    return df