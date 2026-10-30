from pydantic import BaseModel

class CreateEvent(BaseModel):
     title: str
     description: str
     starts_at: str
     ends_at: str
     venue_id: int

class ModifyEvent(BaseModel):
     description: str | None = None
     starts_at: str | None = None
     ends_at: str | None = None