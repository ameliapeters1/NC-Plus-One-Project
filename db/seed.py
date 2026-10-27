from connection import get_connection
from drop_tables import drop_tables
from create_tables import create_tables
from insert_into_tables import insert_info

def seed():
    """
    Initialise and populate the database with seed data.
    Establishes a database connection, drops existing tables, recreates the database
    schema, inserts any initial data and closes the connection upon completion.
    """
    conn = get_connection()
    drop_tables(conn)
    create_tables(conn)
    insert_info(conn)
    conn.close()

seed()
