from pydantic import BaseModel

class Event(BaseModel):
     title: str
     description: str
     starts_at: str
     ends_at: str
     venue_id: int