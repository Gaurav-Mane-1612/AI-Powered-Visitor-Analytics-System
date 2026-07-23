from fastapi import APIRouter, Query

from backend.app.schemas.feedback_schema import FeedbackCreate

from backend.app.services.feedback_service import (
    create_feedback,
    get_all_feedback,
    get_feedback_analytics,
    get_rating_distribution
)

router = APIRouter()


@router.post("/feedback")
def add_feedback(feedback: FeedbackCreate):
    return create_feedback(feedback)


@router.get("/feedback")
def read_all_feedback(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str = "",
    rating: int = 0,
    sort_by: str = "id",
    order: str = "desc"
):

    return get_all_feedback(
        page,
        limit,
        search,
        rating,
        sort_by,
        order
    )


@router.get("/feedback/analytics")
def feedback_analytics():
    return get_feedback_analytics()


@router.get("/feedback/rating-distribution")
def rating_distribution():
    return get_rating_distribution()