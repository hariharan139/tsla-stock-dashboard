# import pandas as pd
# import joblib

# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor

# from services.feature_engineering import prepare_features
# from ml.evaluate import evaluate_model
# from ml.sarima_model import train_sarimax

# df = pd.read_csv(
#     "output/processed_TSLA.csv"
# )

# df['Date'] = pd.to_datetime(df['Date'])

# df.set_index(
#     'Date',
#     inplace=True
# )
# df = df.asfreq('B')
# df = df.ffill().infer_objects(copy=False)
# df = prepare_features(df)

# # Hold last 30 days
# train_df = df[:-30]
# test_df = df[-30:]

# # Features
# X_train = train_df[
#     [
#         'Adj Close',
#         'pct_change',
#         'prev_close',
#         'rolling_mean_5'
#     ]
# ]

# y_train = train_df['target']

# X_test = test_df[
#     [
#         'Adj Close',
#         'pct_change',
#         'prev_close',
#         'rolling_mean_5'
#     ]
# ]

# y_test = test_df['target']

# # ---------------------
# # Linear Regression
# # ---------------------

# lr = LinearRegression()

# lr.fit(X_train, y_train)

# lr_preds = lr.predict(X_test)

# lr_mae, lr_rmse = evaluate_model(
#     y_test,
#     lr_preds
# )

# joblib.dump(
#     lr,
#     "models/lr.pkl"
# )

# # ---------------------
# # Random Forest
# # ---------------------

# rf = RandomForestRegressor(
#     n_estimators=100,
#     random_state=42
# )

# rf.fit(X_train, y_train)

# rf_preds = rf.predict(X_test)

# rf_mae, rf_rmse = evaluate_model(
#     y_test,
#     rf_preds
# )

# joblib.dump(
#     rf,
#     "models/rf.pkl"
# )

# # ---------------------
# # SARIMA
# # ---------------------

# train_exog = train_df[
#     [
#         'pct_change',
#         'prev_close',
#         'rolling_mean_5'
#     ]
# ]

# test_exog = test_df[
#     [
#         'pct_change',
#         'prev_close',
#         'rolling_mean_5'
#     ]
# ]

# sarima_model = train_sarimax(
#     train_df['Adj Close'],
#     train_exog
# )

# sarima_preds = sarima_model.forecast(
#     steps=30,
#     exog=test_exog
# )

# sarima_mae, sarima_rmse = evaluate_model(
#     test_df['Adj Close'],
#     sarima_preds
# )

# # ---------------------
# # Save comparison
# # ---------------------

# results = pd.DataFrame({

#     "Model":[
#         "Linear Regression",
#         "Random Forest",
#         "SARIMA"
#     ],

#     "MAE":[
#         lr_mae,
#         rf_mae,
#         sarima_mae
#     ],

#     "RMSE":[
#         lr_rmse,
#         rf_rmse,
#         sarima_rmse
#     ]

# })

# results.to_csv(
#     "output/comparison_results.csv",
#     index=False
# )

# print(results)

import pandas as pd
import os

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from services.top_companies import get_top_companies
from services.data_processing import process_stock
from services.model_manager import save_model
from services.model_manager import load_model

from ml.evaluate import evaluate_model
from ml.sarimax_model import train_sarimax


TOP_N = 20


companies = get_top_companies(
    TOP_N
)

summary = []


for _, row in companies.iterrows():

    ticker = row['ticker']

    print(
        "Processing:",
        ticker
    )

    try:

        df = process_stock(
            ticker
        )

        train = df[:-30]
        test = df[-30:]

        X_train = train[
            [
                'Adj Close',
                'pct_change',
                'prev_close',
                'rolling_mean_5'
            ]
        ]

        y_train = train[
            'Adj Close'
        ]

        X_test = test[
            [
                'Adj Close',
                'pct_change',
                'prev_close',
                'rolling_mean_5'
            ]
        ]

        y_test = test[
            'Adj Close'
        ]

        # LR

        lr_path = f"models/{ticker}_lr.pkl"

        lr = load_model(
            lr_path
        )

        if lr is None:

            lr = LinearRegression()

            lr.fit(
                X_train,
                y_train
            )

            save_model(
                lr,
                lr_path
            )

        lr_preds = lr.predict(
            X_test
        )

        lr_mae, lr_rmse = evaluate_model(
            y_test,
            lr_preds
        )

        # RF

        rf_path = f"models/{ticker}_rf.pkl"

        rf = load_model(
            rf_path
        )

        if rf is None:

            rf = RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )

            rf.fit(
                X_train,
                y_train
            )

            save_model(
                rf,
                rf_path
            )

        rf_preds = rf.predict(
            X_test
        )

        rf_mae, rf_rmse = evaluate_model(
            y_test,
            rf_preds
        )

        # SARIMAX

        sar_path = f"models/{ticker}_sarimax.pkl"

        sar = load_model(
            sar_path
        )

        if sar is None:

            sar = train_sarimax(

                train['Adj Close'],

                train[
                    [
                        'pct_change',
                        'prev_close',
                        'rolling_mean_5'
                    ]
                ]
            )

            save_model(
                sar,
                sar_path
            )

        sar_preds = sar.forecast(

            steps=30,

            exog=test[
                [
                    'pct_change',
                    'prev_close',
                    'rolling_mean_5'
                ]
            ]
        )

        sar_mae, sar_rmse = evaluate_model(
            y_test,
            sar_preds
        )

        best = min(

            {

                'LR':lr_mae,
                'RF':rf_mae,
                'SARIMAX':sar_mae

            },

            key=lambda k:{

                'LR':lr_mae,
                'RF':rf_mae,
                'SARIMAX':sar_mae

            }[k]
        )

        summary.append({

            'Ticker':ticker,

            'LR_MAE':lr_mae,

            'RF_MAE':rf_mae,

            'SARIMAX_MAE':sar_mae,

            'Best_Model':best

        })

    except Exception as e:

        print(
            ticker,
            e
        )

summary_df = pd.DataFrame(
    summary
)

summary_df.to_csv(

    "output/model_summary.csv",

    index=False

)

print(
    summary_df
)