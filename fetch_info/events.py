from db.connection import get_connection

def get_all_events():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
        SELECT events.id, title, starts_at, ends_at, venues.name 
        FROM events 
        INNER JOIN venues ON events.venue_id = venues.id 
        ORDER BY starts_at ASC""")
        rows = cur.fetchall()
        
    conn.close()
        
    return {"events":[{"id": r[0],
                        "title": r[1],
                        "starts_at": r[2],
                        "ends_at": r[3],
                        "location": r[4]} for r in rows]}


def get_all_events_organised_by_user(user_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
        SELECT id, organiser_id
        FROM events 
        WHERE organiser_id = %s""",
        (user_id,))
        rows = cur.fetchall()
        
    conn.close()
        
    return [row[0] for row in rows]