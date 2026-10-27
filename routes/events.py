from fastapi import APIRouter, HTTPException

from db.connection import get_connection

router = APIRouter(prefix="/api/events", tags=["events"])

@router.get("")
def get_events():
    """
    Retrieve all events ordered by their start time in ascending order.
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT events.id, title, starts_at, ends_at, venues.name 
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

@router.get("/{id}")
def get_event_by_id(id:int):
    """
    Retrieve a single event by its ID.
    """
    if id<=0:
        raise HTTPException(
            status_code=400, 
            detail={"code": "Bad Request"},
        )
    
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""SELECT events.id, title, description, starts_at, ends_at, name, address, capacity, created_at
        FROM events 
        INNER JOIN venues ON events.venue_id = venues.id 
        WHERE events.id = %s
        ORDER BY starts_at ASC""",
        (id,))
        row = cur.fetchone()
    

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "Not Found", "message": "Event not found"},
        )

    conn.close()

    return {"event":{"id": row[0],
                           "title": row[1],
                           "description": row[2],
                           "starts_at": row[3],
                           "ends_at": row[4],
                           "location": row[5],
                           "address": row[6],
                           "capacity": row[7],
                           "created_at": row[8]}}
    
 