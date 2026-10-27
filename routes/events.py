from fastapi import APIRouter, HTTPException

from db.connection import get_connection

router = APIRouter(prefix="/api/events", tags=["events"])

@router.get("")
def get_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT events.id, title, starts_at, ends_at, venues.address 
    FROM events 
    INNER JOIN venues ON events.venue_id = venues.id 
    ORDER BY starts_at ASC""")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"events":[{"id": r[0],
                       "title": r[1],
                       "starts_at": r[2],
                       "ends_at": r[3],
                       "location": r[4]} for r in rows]}
