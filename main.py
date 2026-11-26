from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from routes.events import router as events_router
from routes.auth import router as auth_router
from routes.user import router as user_router

from dotenv import load_dotenv
load_dotenv(".env.development")
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Booking API", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})