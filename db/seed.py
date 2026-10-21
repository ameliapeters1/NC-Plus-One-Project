from connection import get_connection
from drop_tables import drop_tables
from create_tables import create_tables
from insert_into_tables import insert_info

def seed():
    conn = get_connection()
    drop_tables(conn)
    create_tables(conn)
    insert_info(conn)
    conn.close()

seed()
