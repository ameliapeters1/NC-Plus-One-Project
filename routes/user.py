from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from db.connection import get_connection
from validators.validate_credentials import check_credentials

router = APIRouter(prefix="/api/user", tags=["user"])
bearer_scheme = HTTPBearer()


@router.get("/me/events", status_code=200)
def get_my_rsvped_events(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)
):
    """
    Retrieve all events the authenticated user has RSVPed to.
    Includes event rank and total RSVPs.
    """

    user_id = check_credentials(credentials)

    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                events.id,
                events.title,
                events.starts_at,
                rsvps.created_at AS rsvp_date,
                ROW_NUMBER() OVER (
                    ORDER BY events.starts_at ASC
                ) AS event_rank,
                COUNT(*) OVER () AS total_rsvps
            FROM events
            INNER JOIN rsvps
                ON events.id = rsvps.event_id
            WHERE rsvps.attendee_id = %s
            ORDER BY events.starts_at ASC;
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

    conn.close()

    events = [
        {
            "id": row[0],
            "title": row[1],
            "starts_at": row[2],
            "rsvp_date": row[3],
            "event_rank": row[4],
            "total_rsvps": row[5]
        }
        for row in rows
    ]

    return {"events": events}