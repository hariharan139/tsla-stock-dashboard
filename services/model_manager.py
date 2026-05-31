import os
import joblib


def save_model(
    model,
    path
):

    joblib.dump(
        model,
        path
    )


def load_model(path):

    if os.path.exists(path):

        return joblib.load(path)

    return None