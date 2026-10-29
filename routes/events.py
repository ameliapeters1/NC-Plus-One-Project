from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from db.connection import get_connection
from auth.passwords import get_secret



router = APIRouter(prefix="/api/events", tags=["events"])
bearer_scheme = HTTPBearer()

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
    
@router.post("/{event_id}/rsvp", status_code= 201)
def rsvp(event_id: int, 
         credentials : HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    """
    RSVP to an event by ID as an authenticated user.
    """
    conn = get_connection()

    # check credentials
    unauthorised = HTTPException(
        status_code=401, 
        detail = {"code":"Not Authenticated"},
        headers = {"WWW-Authenticate": "Bearer"})

    if credentials is None:
        raise unauthorised

    try: 
        payload = jwt.decode(credentials.credentials, get_secret(), algorithms=["HS256"])
        user_id = int(payload["sub"])

    except: # not valid credentials
        raise unauthorised


    with conn.cursor() as cur:
        cur.execute("""SELECT events.id, title, starts_at, ends_at, venues.name 
        FROM events 
        INNER JOIN venues ON events.venue_id = venues.id 
        ORDER BY starts_at ASC""")
        rows = cur.fetchall()
    event_ids = [row[0] for row in rows]
        
    if event_id not in event_ids:
        raise HTTPException(status_code=404,
                            detail={"code":"Not Found", "message": "event not found"})

    with conn.cursor() as cursor:
        cursor.execute("""SELECT id, attendee_id, event_id, created_at
                    FROM rsvps 
                    WHERE attendee_id = %s AND event_id = %s""",
                    (user_id,event_id))
        already_rsvp = cursor.fetchall()
    if already_rsvp:
        raise HTTPException(status_code=409,
                            detail={"code":"Conflict", "message":"Already RSVPed"})


    
    insert_statement = " INSERT INTO rsvps (attendee_id, event_id) VALUES (%s,%s); "
    with conn.cursor() as cursor:
        cursor.execute(insert_statement,(user_id, event_id))
        conn.commit()

        cursor.execute("""SELECT id, attendee_id, event_id, created_at
                    FROM rsvps 
                    WHERE attendee_id = %s AND event_id = %s""",
                    (user_id,event_id))
        row = cursor.fetchone()
        rsvp = {"id":row[0],
                "attendee_id":row[1],
                "event_id":row[2],
                "created_at":row[3]}

        conn.close

        return {"rsvp": rsvp}

    