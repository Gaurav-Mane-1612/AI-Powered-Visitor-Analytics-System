from pydantic import BaseModel
from typing import Optional


class VisitCreate(BaseModel):
    visitor_id: int
    purpose: str
    person_to_meet: str
    department: Optional[str] = None
    