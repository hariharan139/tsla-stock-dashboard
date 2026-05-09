import sqlite3

def get_connection():
    return sqlite3.connect("stock.db")

def init_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        date TEXT,
        adj_close REAL,
        pct_change REAL
    )
    """)

    conn.close()


def insert_data(df):
    conn = sqlite3.connect("stock.db")

    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO stock_data (date, adj_close, pct_change, month_change)
            VALUES (?, ?, ?, ?)
        """, (
            str(row['Date']),
            row['Adj Close'],
            row['pct_change'],
            row['1monthchange']
        ))

    conn.commit()
    conn.close()


def fetch_data():
    conn = sqlite3.connect("stock.db")
    data = conn.execute("SELECT * FROM stock_data ORDER BY date DESC LIMIT 50").fetchall()
    conn.close()
    return data