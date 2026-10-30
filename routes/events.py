from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime

from db.connection import get_connection
from models.events import CreateEvent, ModifyEvent
from validators.validate_credentials import check_credentials
from fetch_info.rsvp import get_rsvp
from validators.validate_time import check_time_format
from fetch_info.venues import get_venue_ids
from fetch_info.events import get_all_events, get_all_events_organised_by_user

router = APIRouter(prefix="/api/events", tags=["events"])
bearer_scheme = HTTPBearer()


@router.get("")
def get_events():
    """
    Retrieve all events ordered by their start time in ascending order.
    """
    events = get_all_events()
    return events

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

    user_id = check_credentials(credentials)

    all_events = get_all_events()
    event_ids = [event["id"] for event in all_events["events"]]
        
    if event_id not in event_ids:
        raise HTTPException(status_code=404,
                            detail={"code":"Not Found", "message": "event not found"})

    already_rsvp = get_rsvp(user_id, event_id)

    if already_rsvp:
        raise HTTPException(status_code=409,
                            detail={"code":"Conflict", "message":"Already RSVPed"})


    
    insert_statement = " INSERT INTO rsvps (attendee_id, event_id) VALUES (%s,%s); "
    with conn.cursor() as cursor:
        cursor.execute(insert_statement,(user_id, event_id))
        conn.commit()
    conn.close()

    created_rsvp = get_rsvp(user_id, event_id)
    return {"rsvp": created_rsvp}

@router.delete("/{event_id}/rsvp/me", status_code= 204)
def delete_rsvp(event_id: int, 
         credentials : HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    """
    Delete an event RSVP by event ID as an authenticated user.
    """
    conn = get_connection()

    user_id = check_credentials(credentials)
    rsvp = get_rsvp(user_id, event_id)

    if rsvp is None:
        raise HTTPException(status_code=404,
                            detail={"code":"Not Found", "message": "not RSVPed to event"})

    with conn.cursor() as cursor:
        cursor.execute(f"DELETE FROM rsvps WHERE attendee_id = '{user_id}' AND event_id = '{event_id}'")
        conn.commit()
    conn.close()

@router.post("", status_code= 201)
def add_event(body: CreateEvent,
         credentials : HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    """
    Create a new event as an authenticated user.
    """
    conn = get_connection()

    if not body.title or not body.starts_at or not body.ends_at:
            raise HTTPException(status_code=400,
                                detail={"code": "Bad Request"})

    if check_time_format(body.starts_at) is False or check_time_format(body.ends_at) is False:
        raise HTTPException(status_code=400,
                            detail={"code":"Bad Request", "message": "Dates must be valid ISO 8601 strings"})

    user_id = check_credentials(credentials)

    venues = get_venue_ids()
    if body.venue_id not in venues:
        raise HTTPException(status_code=404,
                            detail={"code":"Not Found", "message":"Venue ID not found"})

    if body.starts_at > body.ends_at:
        raise HTTPException(status_code=400,
                            detail={"code":"Bad Request", "message":"Start time should be earlier than end time"})

    insert_statement = """
    INSERT INTO events (title, description, starts_at, ends_at, organiser_id, venue_id) 
    VALUES (%s,%s,%s,%s,%s,%s)
    RETURNING *;"""
    with conn.cursor() as cursor:
        cursor.execute(insert_statement, (body.title, body.description, body.starts_at, body.ends_at, user_id, body.venue_id))
        added_event = cursor.fetchone()
        conn.commit()
    conn.close()
    return added_event

@router.patch("/{event_id}", status_code=200)
def modify_event(event_id, body: ModifyEvent,
                 credentials : HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):
    event_id = int(event_id)
    user_id = check_credentials(credentials)
    
    all_events = get_all_events()
    event_ids = [event["id"] for event in all_events["events"]]
    if event_id not in event_ids:
        print(event_id)
        raise HTTPException(status_code=404,
                            detail={"code":"Not Found", "message":"event not found"})


    events_for_user = get_all_events_organised_by_user(user_id)
    if event_id not in events_for_user:
         raise HTTPException(status_code=403,
                             detail={"code":"Forbidden", "message":"Authenticated user not the organiser of the event"})


    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT starts_at, ends_at FROM events WHERE id=%s;", (event_id,))
        current_event = cursor.fetchone()
        current_starts_at = current_event[0]
        current_ends_at = current_event[1]
        if body.starts_at:
            if check_time_format(body.starts_at) is False:
                raise HTTPException(status_code=400,
                                    detail={"code":"Bad Request", "message": "Dates must be valid ISO 8601 strings"})
            new_start = datetime.fromisoformat(body.starts_at)
        else:
            new_start = current_starts_at

        if body.ends_at:
            if check_time_format(body.ends_at) is False:
                raise HTTPException(status_code=400,
                                    detail={"code":"Bad Request", "message": "Dates must be valid ISO 8601 strings"})
            new_end = datetime.fromisoformat(body.ends_at)
        else:
            new_end = current_ends_at

        if new_start >= new_end:
            raise HTTPException(status_code=400,
                                detail={"code": "Bad Request", "message": "Start time must be before end time"})
    
        if body.description:
            cursor.execute("UPDATE events SET description = %s WHERE id=%s;",(body.description,event_id)) 
        if body.starts_at:
            cursor.execute("UPDATE events SET starts_at = %s WHERE id=%s;",(new_start,event_id))
        if body.ends_at:
            cursor.execute("UPDATE events SET ends_at = %s WHERE id=%s;",(new_end,event_id))
        conn.commit()

        cursor.execute("""
        SELECT * FROM events 
        WHERE id = %s;""", (event_id,))
        event = cursor.fetchone()
    return {"event":{"id": event[0],
      "title": event[1],
      "description": event[2],
      "starts_at":event[3],
      "ends_at": event[4],
      "venue_id": event[5],
      "organiser_id": event[6],
      "created_at": event[7]}}