from sklearn.metrics import mean_absolute_error, r2_score

def evaluate(y_true, y_pred):

    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print("MAE:", mae)
    print("R2 Score:", r2)