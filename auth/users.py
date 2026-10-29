from db.connection import get_connection
from fastapi import HTTPException
import jwt
from auth.passwords import get_secret

def get_user(email):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s",
                            (email,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], 
                "email": row[1],
                "password_hash": row[2],
                "name":row[3],}

def check_credentials(credentials):
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

    return user_id
    