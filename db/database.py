import sqlite3


def get_connection():

    conn = sqlite3.connect(
        "database/stocks.db"
    )

    return conn


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS stocks(

        ticker TEXT,
        date TEXT,
        adj_close REAL,
        pct_change REAL

        )
        '''
    )

    conn.commit()

    conn.close()