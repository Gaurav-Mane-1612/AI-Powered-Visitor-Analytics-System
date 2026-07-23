from fastapi import APIRouter, Query

from backend.app.schemas.visitor_schema import VisitorCreate

from backend.app.services.visitor_service import (
    create_visitor,
    get_all_visitors,
    get_visitor_by_id,
    update_visitor,
    delete_visitor
)

router = APIRouter()


@router.post("/visitors")
def register_visitor(visitor: VisitorCreate):
    return create_visitor(visitor)


@router.get("/visitors")
def fetch_all_visitors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str = "",
    organization: str = "",
    sort_by: str = "id",
    order: str = "desc"
):

    return get_all_visitors(
        page,
        limit,
        search,
        organization,
        sort_by,
        order
    )


@router.get("/visitors/{visitor_id}")
def fetch_visitor(visitor_id: int):
    return get_visitor_by_id(visitor_id)


@router.put("/visitors/{visitor_id}")
def update_visitor_data(visitor_id: int, visitor: VisitorCreate):

    updated = update_visitor(visitor_id, visitor)

    if updated:
        return {
            "status": "success",
            "message": "Visitor updated successfully"
        }

    return {
        "status": "error",
        "message": "Visitor not found"
    }


@router.delete("/visitors/{visitor_id}")
def delete_visitor_api(visitor_id: int):

    deleted = delete_visitor(visitor_id)

    if not deleted:
        return {
            "status": "error",
            "message": "Visitor not found"
        }

    return {
        "status": "success",
        "message": "Visitor deleted successfully"
    }