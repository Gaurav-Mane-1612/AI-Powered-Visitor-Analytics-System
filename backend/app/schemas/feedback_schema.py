from pydantic import BaseModel, Field
from typing import Optional


class FeedbackCreate(BaseModel):
    visit_id: int
    rating: int = Field(..., ge=1, le=5)
    feedback: Optional[str] = None