import json 

def load_json(filepath):
    with open(filepath) as file:
        return  json.load(file)

def insert_user_info(conn):
    users = load_json("./db/data/users.json")
    insert_statement_users = """ INSERT INTO users (email, password, name) VALUES (%s,%s,%s); """
    
    with conn.cursor() as cursor:
        for user in users:
            cursor.execute(insert_statement_users,
                       (user["email"], user["password"],user["name"]))
    

def insert_venue_info(conn):
    venues = load_json("./db/data/venues.json")
    insert_statement_venues = """ INSERT INTO venues (name, address, capacity) VALUES (%s,%s,%s); """
    
    with conn.cursor() as cursor:
        for venue in venues:
            cursor.execute(insert_statement_venues,
                           (venue["name"], venue["address"],venue["capacity"]))
            

def insert_event_info(conn):
    events = load_json("./db/data/events.json")
    insert_statement_events = """ INSERT INTO events 
                (title, description, starts_at, ends_at, organiser_id, venue_id) VALUES (%s,%s,%s,%s,%s,%s); """
    
    with conn.cursor() as cursor:
        for event in events:
            cursor.execute(insert_statement_events,
                            (event["title"], event["description"],event["starts_at"],
                            event["ends_at"], event["organiser_id"], event["venue_id"]))
            

def insert_rsvp_info(conn):
    rsvps = load_json("./db/data/rsvps.json")
    insert_statement_rsvps = """ INSERT INTO rsvps 
                (attendee_id, event_id) VALUES (%s,%s); """
    with conn.cursor() as cursor:
        for rsvp in rsvps:
            cursor.execute(insert_statement_rsvps,
                       (rsvp["attendee_id"], rsvp["event_id"]))
    

def insert_info(conn):
    """
    Insert all data into the appropriate tables of the database.
    """
    insert_user_info(conn)
    insert_venue_info(conn)
    insert_event_info(conn)
    insert_rsvp_info(conn)
    conn.commit()
    