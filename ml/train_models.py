import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from services.feature_engineering import prepare_features
from ml.evaluate import evaluate_model
from ml.sarima_model import train_sarimax

df = pd.read_csv(
    "output/processed_TSLA.csv"
)

df['Date'] = pd.to_datetime(df['Date'])

df.set_index(
    'Date',
    inplace=True
)
df = df.asfreq('B')
df = df.ffill().infer_objects(copy=False)
df = prepare_features(df)

# Hold last 30 days
train_df = df[:-30]
test_df = df[-30:]

# Features
X_train = train_df[
    [
        'Adj Close',
        'pct_change',
        'prev_close',
        'rolling_mean_5'
    ]
]

y_train = train_df['target']

X_test = test_df[
    [
        'Adj Close',
        'pct_change',
        'prev_close',
        'rolling_mean_5'
    ]
]

y_test = test_df['target']

# ---------------------
# Linear Regression
# ---------------------

lr = LinearRegression()

lr.fit(X_train, y_train)

lr_preds = lr.predict(X_test)

lr_mae, lr_rmse = evaluate_model(
    y_test,
    lr_preds
)

joblib.dump(
    lr,
    "models/lr.pkl"
)

# ---------------------
# Random Forest
# ---------------------

rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf.fit(X_train, y_train)

rf_preds = rf.predict(X_test)

rf_mae, rf_rmse = evaluate_model(
    y_test,
    rf_preds
)

joblib.dump(
    rf,
    "models/rf.pkl"
)

# ---------------------
# SARIMA
# ---------------------

train_exog = train_df[
    [
        'pct_change',
        'prev_close',
        'rolling_mean_5'
    ]
]

test_exog = test_df[
    [
        'pct_change',
        'prev_close',
        'rolling_mean_5'
    ]
]

sarima_model = train_sarimax(
    train_df['Adj Close'],
    train_exog
)

sarima_preds = sarima_model.forecast(
    steps=30,
    exog=test_exog
)

sarima_mae, sarima_rmse = evaluate_model(
    test_df['Adj Close'],
    sarima_preds
)

# ---------------------
# Save comparison
# ---------------------

results = pd.DataFrame({

    "Model":[
        "Linear Regression",
        "Random Forest",
        "SARIMA"
    ],

    "MAE":[
        lr_mae,
        rf_mae,
        sarima_mae
    ],

    "RMSE":[
        lr_rmse,
        rf_rmse,
        sarima_rmse
    ]

})

results.to_csv(
    "output/comparison_results.csv",
    index=False
)

print(results)