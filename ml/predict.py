import joblib

def load_model():
    return joblib.load("models/stock_model.pkl")


def predict_price(data):

    model = load_model()

    prediction = model.predict([[
        data['Adj Close'],
        data['pct_change'],
        data['prev_close'],
        data['rolling_mean_5']
    ]])

    return prediction[0]