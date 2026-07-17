from pydantic import BaseModel, EmailStr
from typing import Optional


class VisitorCreate(BaseModel):
    full_name: str
    mobile: str
    email: Optional[EmailStr] = None
    organization: Optional[str] = None
    address: Optional[str] = None
    