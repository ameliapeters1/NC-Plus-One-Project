import os
import bcrypt
from datetime import datetime, timezone, timedelta
import jwt

ALGORITHM = "HS256"

def hash_password(password:str) -> str:
    rounds = 4 if os.getenv("ENV")=="test" else 12
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt(rounds)).decode()

def verify_password(password:str, hashed_password:str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def get_secret():
    secret = os.getenv("JWT_SECRET")
    return secret

def create_access_token(id:int)->str:
    payload ={
        "sub":str(id),
        "exp": datetime.now(timezone.utc)+timedelta(hours=1)
    }

    return jwt.encode(payload, get_secret(), algorithm=ALGORITHM)