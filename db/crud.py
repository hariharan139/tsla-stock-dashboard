from db.database import get_connection


def insert_stock(df, ticker):

    conn = get_connection()

    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(
            '''
            INSERT INTO stocks
            VALUES(?,?,?,?)
            ''',
            (
                ticker,
                str(row['Date']),
                float(row['Adj Close']),
                float(row['pct_change'])
            )
        )

    conn.commit()
    conn.close()


def fetch_stock(ticker):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT * FROM stocks
        WHERE ticker=?
        ''',
        (ticker,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows