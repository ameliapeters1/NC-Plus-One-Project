from fastapi import HTTPException
from auth.passwords import get_secret
import jwt

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
    