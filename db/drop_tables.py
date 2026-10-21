def drop_tables(conn):
    cursor = conn.cursor()
    tables = ["rsvps", "events", "venues","users"]
    for table in tables:
        drop = f"DROP TABLE IF EXISTS {table};"
        cursor.execute(drop)
    cursor.close()