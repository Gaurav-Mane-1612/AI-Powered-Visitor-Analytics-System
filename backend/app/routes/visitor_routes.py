from fastapi import APIRouter
from backend.app.schemas.visitor_schema import VisitorCreate
from backend.app.services.visitor_service import create_visitor, get_all_visitors

router = APIRouter()


@router.post("/visitors")
def register_visitor(visitor: VisitorCreate):
    return create_visitor(visitor)


@router.get("/visitors")
def fetch_all_visitors():
    return get_all_visitors()