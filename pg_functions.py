import psycopg2

def pg_connect():
    """
    Create and return a new Postgres connection.
    Current function is hardcoded with server information.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="password",
            port="5432"
        )
        print("Connection successful!")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def pg_disconnect(conn):
    """
    Close the given connection.
    Failure to do so will create memory leaks.
    Call this after connecting to the server and completing your function.
    """
    if conn:
        conn.close()
        print("PostgreSQL connection is closed")
