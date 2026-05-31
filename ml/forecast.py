# import pandas as pd
# import joblib
# import matplotlib.pyplot as plt

# # Models
# lr = joblib.load(
#     "models/lr.pkl"
# )

# rf = joblib.load(
#     "models/rf.pkl"
# )

# sarima = joblib.load(
#     "models/sarima.pkl"
# )

# # Load data
# df = pd.read_csv(
#     "output/processed_TSLA.csv"
# )

# # Features
# df['prev_close'] = df['Adj Close'].shift(1)

# df['rolling_mean_5'] = (
#     df['Adj Close']
#     .rolling(5)
#     .mean()
# )

# df.dropna(inplace=True)

# # Last 30 days
# test = df[-30:]

# X_test = test[
#     [
#         'Adj Close',
#         'pct_change',
#         'prev_close',
#         'rolling_mean_5'
#     ]
# ]

# actual = test['Adj Close']

# # Predictions
# lr_preds = lr.predict(X_test)

# rf_preds = rf.predict(X_test)

# sarima_preds = sarima.forecast(
#     steps=30,
#     exog=X_test[
#         [
#             'pct_change',
#             'prev_close',
#             'rolling_mean_5'
#         ]
#     ]
# )

# # Save results
# result = pd.DataFrame({

#     "Actual":
#         actual.values,

#     "LR":
#         lr_preds,

#     "RF":
#         rf_preds,

#     "SARIMAX":
#         sarima_preds.values

# })

# result.to_csv(
#     "output/forecast_results.csv",
#     index=False
# )

# # Plot
# plt.figure(figsize=(12,6))

# plt.plot(
#     actual.values,
#     label="Actual",
#     linewidth=3
# )

# plt.plot(
#     lr_preds,
#     label="Linear Regression",
#     linestyle='--'
# )

# plt.plot(
#     rf_preds,
#     label="Random Forest",
#     linestyle='-.'
# )

# plt.plot(
#     sarima_preds.values,
#     label="SARIMAX",
#     linestyle=':'
# )

# plt.legend()

# plt.title(
#     "30-Day Stock Forecast Comparison"
# )

# plt.xlabel("Days")
# plt.ylabel("Adj Close Price")

# plt.grid(True)

# plt.tight_layout()

# plt.savefig(
#     "static/forecast_graph.png",
#     dpi=300
# )
import os
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from services.data_processing import process_stock
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from ml.sarimax_model import train_sarimax
from services.model_manager import save_model

def generate_forecast(
    ticker
):

    df = process_stock(
        ticker
    )

    test = df[-30:]

    X_test = test[
        [
            'Adj Close',
            'pct_change',
            'prev_close',
            'rolling_mean_5'
        ]
    ]

    actual = test[
        'Adj Close'
    ]

    lr = joblib.load(
        f"models/{ticker}_lr.pkl"
    )

    rf = joblib.load(
        f"models/{ticker}_rf.pkl"
    )

    sar = joblib.load(
        f"models/{ticker}_sarimax.pkl"
    )

    lr_preds = lr.predict(
        X_test
    )

    rf_preds = rf.predict(
        X_test
    )

    sar_preds = sar.forecast(

        steps=30,

        exog=X_test[
            [
                'pct_change',
                'prev_close',
                'rolling_mean_5'
            ]
        ]
    )

    plt.figure(
        figsize=(12,6)
    )

    plt.plot(
        actual.values,
        label='Actual',
        linewidth=3
    )

    plt.plot(
        lr_preds,
        label='LR'
    )

    plt.plot(
        rf_preds,
        label='RF'
    )

    plt.plot(
        sar_preds.values,
        label='SARIMAX'
    )

    plt.legend()

    plt.grid(True)

    plt.title(
        f"{ticker} Forecast"
    )
    plt.savefig(
    f"static/graphs/{ticker}.png"
)
    result = pd.DataFrame({

    'Actual':
        actual.values.flatten(),

    'LR':
        lr_preds.flatten(),

    'RF':
        rf_preds.flatten(),

    'SARIMAX':
        sar_preds.values.flatten()

})

    result.to_csv(

        f"output/forecast_results/{ticker}.csv",

        index=False
    )