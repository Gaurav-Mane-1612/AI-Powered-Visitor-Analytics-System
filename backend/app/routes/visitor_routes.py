from fastapi import APIRouter
from backend.app.schemas.visitor_schema import VisitorCreate

router = APIRouter()

@router.post("/visitors")
def create_visitor(visitor: VisitorCreate):
    return {
        "message": "Visitor data received successfully",
        "data": visitor
    }