import os
os.environ["ENV"] = "development"

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth.users import get_user
from auth.passwords import verify_password, create_access_token
from db.connection import get_connection


router = APIRouter(prefix="/api/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email:str
    password:str

@router.post("/login")
def login(body:LoginRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=400,
                            detail={"code": "Bad Request"})
    
    user = get_user(body.email)
    print(user)

  
    if user is not None and verify_password(body.password,user["password_hash"]): 
            return {
            "token": create_access_token(user["id"]),
            }
    else:
        raise HTTPException(status_code=401,
                            detail={"code": "Unauthorised", "message":"Email and/or password incorrect"})