import os
os.environ["ENV"] = "development"

from fastapi import APIRouter, HTTPException

from models.users import LoginRequest, RegisterRequest
from fetch_info.users import get_user
from auth.passwords import verify_password, create_access_token, hash_password
from db.connection import get_connection

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
def login(body:LoginRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=400,
                            detail={"code": "Bad Request"})
    
    user = get_user(body.email)
  
    if user is not None and verify_password(body.password,user["password_hash"]): 
            return {
            "token": create_access_token(user["id"]),
            }
    else:
        raise HTTPException(status_code=401,
                            detail={"code": "Unauthorised", "message":"Email and/or password incorrect"})

@router.post("/register", status_code= 201)
def register(body:RegisterRequest):
    conn = get_connection()
    name = body.name
    email = body.email
    password = body.password

    if not name or not email or not password:
        raise HTTPException(status_code=400,
                            detail={"code": "Bad Request", "message":"Missing required field(s)"})

    if get_user(email) is not None:
         raise HTTPException(status_code=409,
                             detail={"code": "Conflict", "message":"Email already registered"})


    insert_statement = """INSERT INTO users (email, password, name) VALUES (%s,%s,%s);"""

    with conn.cursor() as cursor:
        cursor.execute(insert_statement, (email, hash_password(password), name))
        conn.commit()
        user = get_user(email)

    conn.close()

    return {"user":user}