from db.connection import get_connection

def get_venue_ids():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM venues")
        venues = cursor.fetchall()
    all_venues = [venue[0] for venue in venues]
    conn.close()
    return all_venues
