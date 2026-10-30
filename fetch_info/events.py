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

def get_most_recently_created_event_by_user(user_id):
    conn = get_connection()
    with conn.cursor() as cursor:
         cursor.execute("""
            SELECT * FROM events
            WHERE organiser_id = %s
            ORDER BY created_at DESC
            LIMIT 1""", (user_id,))
    row = cursor.fetchone()
    conn.close()
        
    return  {"events":{"id": row[0],
                       "title": row[1],
                       "description":row[2],
                       "starts_at": row[3],
                       "ends_at": row[4],
                       "organiser_id": row[5],
                       "venue_id": row[6],
                       "created_at":row[7]}}
