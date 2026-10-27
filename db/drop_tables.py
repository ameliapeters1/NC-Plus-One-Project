def drop_tables(conn):
    """
    Drop the database tables required to enable them to be freshly created. 
    """ 
    cursor = conn.cursor()
    tables = ["rsvps", "events", "venues","users"]
    for table in tables:
        drop = f"DROP TABLE IF EXISTS {table};"
        cursor.execute(drop)
    cursor.close()