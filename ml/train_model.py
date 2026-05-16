import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from services.feature_engineering import prepare_features


# Load data
df = pd.read_csv("output/processed_TSLA.csv")

# Prepare features
df = prepare_features(df)

# Features and target
X = df[['Adj Close', 'pct_change', 'prev_close', 'rolling_mean_5']]
y = df['target']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# -------------------------
# Linear Regression
# -------------------------

lr = LinearRegression()
lr.fit(X_train, y_train)

lr_preds = lr.predict(X_test)

lr_error = mean_absolute_error(y_test, lr_preds)

print("Linear Regression MAE:", lr_error)

# -------------------------
# Random Forest
# -------------------------

rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

rf.fit(X_train, y_train)

rf_preds = rf.predict(X_test)

rf_error = mean_absolute_error(y_test, rf_preds)

print("Random Forest MAE:", rf_error)

# -------------------------
# Choose Best Model
# -------------------------

best_model = rf if rf_error < lr_error else lr

joblib.dump(best_model, "models/stock_model.pkl")

print("Best model saved!")