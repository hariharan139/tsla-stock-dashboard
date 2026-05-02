from flask import Flask, render_template
from services.data_processing import process_data, create_graph
from db import init_db, insert_data, fetch_data
import pandas as pd

app = Flask(__name__)

init_db()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/run')
def run():
    df, monthly = process_data()
    create_graph(monthly)
    return "✅ Data Processed!"


@app.route('/preview')
def preview():
    df = pd.read_csv("output/processed_TSLA.csv")
    return df.head(20).to_html()


@app.route('/store')
def store():
    df, _ = process_data()
    insert_data(df)
    return "✅ Stored in SQLite!"


@app.route('/db')
def view_db():
    data = fetch_data()
    return str(data)


if __name__ == "__main__":
    app.run(debug=True)