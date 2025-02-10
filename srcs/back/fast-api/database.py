import psycopg2
from psycopg2.extensions import connection as _connection

def get_connection() -> _connection:
    return psycopg2.connect(
        dbname="your_db_name",
        user="your_db_user",
        password="your_db_password",
        host="your_db_host",
        port="your_db_port"
    )
