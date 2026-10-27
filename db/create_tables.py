def create_tables(conn):
    """
    Create the database tables required. 
    Creates four tables: 
        - users: stores user account details,
        - venues: stores venue information and capacity
        - events: stores event details, organisers and venue references
        - rsvps: stores user reservations for events.
    """
    with conn.cursor() as cursor:
        users = """ CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL, 
                    created_at TIMESTAMPTZ DEFAULT NOW()
                    ); """
        
        venues = """ CREATE TABLE venues (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL, 
                    address TEXT, 
                    capacity INT
                    ); """

        events = """ CREATE TABLE events (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL, 
                    description VARCHAR(255), 
                    starts_at TIMESTAMPTZ NOT NULL, 
                    ends_at TIMESTAMPTZ NOT NULL,
                    organiser_id INT REFERENCES users(id),
                    venue_id INT REFERENCES venues(id),
                    created_at TIMESTAMPTZ DEFAULT NOW()
                    ); """

        rsvps = """ CREATE TABLE rsvps (
                    id SERIAL PRIMARY KEY,
                    attendee_id INT REFERENCES users(id),
                    event_id INT REFERENCES events(id),
                    created_at TIMESTAMPTZ DEFAULT NOW()
                    ); """

        cursor.execute(users)
        cursor.execute(venues)
        cursor.execute(events)
        cursor.execute(rsvps)
        conn.commit()
   