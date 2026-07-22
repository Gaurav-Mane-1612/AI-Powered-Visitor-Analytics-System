from fastapi import APIRouter, Depends

from backend.app.auth.auth_bearer import JWTBearer
from backend.app.services.dashboard_service import get_dashboard_statistics

router = APIRouter()


@router.get("/dashboard")
def dashboard(token=Depends(JWTBearer())):
    return get_dashboard_statistics()