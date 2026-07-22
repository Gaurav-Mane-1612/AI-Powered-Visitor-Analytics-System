from fastapi import APIRouter
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
def read_all_feedback():
    return get_all_feedback()


@router.get("/feedback/analytics")
def feedback_analytics():
    return get_feedback_analytics()


@router.get("/feedback/rating-distribution")
def rating_distribution():
    return get_rating_distribution()