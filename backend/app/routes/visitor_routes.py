from fastapi import APIRouter
from backend.app.schemas.visitor_schema import VisitorCreate
from backend.app.services.visitor_service import create_visitor

router = APIRouter()


@router.post("/visitors")
def register_visitor(visitor: VisitorCreate):
    return create_visitor(visitor)