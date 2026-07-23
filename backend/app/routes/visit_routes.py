from fastapi import APIRouter, Query

from backend.app.schemas.visit_schema import VisitCreate

from backend.app.services.visit_service import (
    create_visit,
    get_all_visits,
    get_visit_by_id,
    checkout_visit
)

router = APIRouter()


@router.post("/visits")
def register_visit(visit: VisitCreate):
    return create_visit(visit)


@router.get("/visits")
def read_all_visits(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str = "",
    department: str = "",
    person_to_meet: str = "",
    sort_by: str = "id",
    order: str = "desc"
):

    return get_all_visits(
        page,
        limit,
        search,
        department,
        person_to_meet,
        sort_by,
        order
    )


@router.get("/visits/{visit_id}")
def read_visit(visit_id: int):
    return get_visit_by_id(visit_id)


@router.put("/visits/{visit_id}/checkout")
def visitor_checkout(visit_id: int):
    return checkout_visit(visit_id)