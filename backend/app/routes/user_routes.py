from fastapi import APIRouter, Depends

from backend.app.auth.auth_bearer import JWTBearer

from backend.app.schemas.user_schema import UserCreate
from backend.app.schemas.auth_schema import LoginRequest

from backend.app.services.user_service import (
    register_user,
    get_all_users,
    login_user
)

router = APIRouter()


@router.post("/users/register")
def create_user(user: UserCreate):
    return register_user(user)


@router.get("/users")
def read_all_users():
    return get_all_users()


@router.post("/login")
def login(login_data: LoginRequest):
    return login_user(login_data)


# Current Logged-in User
@router.get("/me")
def current_user(token=Depends(JWTBearer())):
    return {
        "status": "success",
        "user": token
    }