from flask import Flask, render_template
from services.data_processing import process_data, create_graph
from db import init_db, insert_data, fetch_data
from routes.stock_routes import stock_bp   # ✅ IMPORTANT (Week 2)

import pandas as pd

app = Flask(__name__)

# Initialize database
init_db()

# Register Week 2 routes
app.register_blueprint(stock_bp)

# -------------------------
# WEEK 1 ROUTES
# -------------------------

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

    
# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":
    app.run(debug=True) 