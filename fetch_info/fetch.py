from db.connection import get_connection

def get_rsvp(user_id, event_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""SELECT id, attendee_id, event_id, created_at
                    FROM rsvps 
                    WHERE attendee_id = %s AND event_id = %s""",
                    (user_id,event_id))
        row = cursor.fetchone()
    if row:
        rsvp = {"id":row[0],
            "attendee_id":row[1],
            "event_id":row[2],
            "created_at":row[3]}
    else:
        rsvp = None
    conn.close()
    return rsvp
