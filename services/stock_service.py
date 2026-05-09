from db import get_connection

def save_stock_data(symbol, df):
    conn = get_connection()

    for _, row in df.iterrows():
        conn.execute("""
        INSERT INTO stocks (symbol, date, adj_close, pct_change)
        VALUES (?, ?, ?, ?)
        """, (
            symbol,
            str(row['Date']),
            row['Adj Close'],
            row['pct_change']
        ))

    conn.commit()
    conn.close()


def get_all_stocks():
    conn = get_connection()
    data = conn.execute("SELECT * FROM stocks ORDER BY date DESC").fetchall()
    conn.close()
    return data


def delete_stock(stock_id):
    conn = get_connection()
    conn.execute("DELETE FROM stocks WHERE id=?", (stock_id,))
    conn.commit()
    conn.close()


def update_stock(stock_id, value):
    conn = get_connection()
    conn.execute("UPDATE stocks SET adj_close=? WHERE id=?", (value, stock_id))
    conn.commit()
    conn.close()