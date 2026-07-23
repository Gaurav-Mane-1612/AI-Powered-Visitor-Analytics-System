from fastapi import APIRouter

from backend.app.services.audit_service import get_all_audit_logs

router = APIRouter()


@router.get("/audit-logs")
def audit_logs():

    return get_all_audit_logs()