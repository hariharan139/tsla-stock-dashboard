from statsmodels.tsa.statespace.sarimax import SARIMAX


def train_sarimax(
    train_y,
    train_exog
):

    model = SARIMAX(

        train_y,

        exog=train_exog,

        order=(1,1,1),

        seasonal_order=(0,1,1,5),

        enforce_stationarity=False,

        enforce_invertibility=False

    )

    fitted = model.fit(
        disp=False,
        maxiter=200
    )

    return fitted