import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Models
lr = joblib.load(
    "models/lr.pkl"
)

rf = joblib.load(
    "models/rf.pkl"
)

sarima = joblib.load(
    "models/sarima.pkl"
)

# Load data
df = pd.read_csv(
    "output/processed_TSLA.csv"
)

# Features
df['prev_close'] = df['Adj Close'].shift(1)

df['rolling_mean_5'] = (
    df['Adj Close']
    .rolling(5)
    .mean()
)

df.dropna(inplace=True)

# Last 30 days
test = df[-30:]

X_test = test[
    [
        'Adj Close',
        'pct_change',
        'prev_close',
        'rolling_mean_5'
    ]
]

actual = test['Adj Close']

# Predictions
lr_preds = lr.predict(X_test)

rf_preds = rf.predict(X_test)

sarima_preds = sarima.forecast(
    steps=30,
    exog=X_test[
        [
            'pct_change',
            'prev_close',
            'rolling_mean_5'
        ]
    ]
)

# Save results
result = pd.DataFrame({

    "Actual":
        actual.values,

    "LR":
        lr_preds,

    "RF":
        rf_preds,

    "SARIMAX":
        sarima_preds.values

})

result.to_csv(
    "output/forecast_results.csv",
    index=False
)

# Plot
plt.figure(figsize=(12,6))

plt.plot(
    actual.values,
    label="Actual",
    linewidth=3
)

plt.plot(
    lr_preds,
    label="Linear Regression",
    linestyle='--'
)

plt.plot(
    rf_preds,
    label="Random Forest",
    linestyle='-.'
)

plt.plot(
    sarima_preds.values,
    label="SARIMAX",
    linestyle=':'
)

plt.legend()

plt.title(
    "30-Day Stock Forecast Comparison"
)

plt.xlabel("Days")
plt.ylabel("Adj Close Price")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "static/forecast_graph.png",
    dpi=300
)