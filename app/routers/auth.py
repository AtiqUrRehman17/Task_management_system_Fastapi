from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.user import UserCreate, UserResponse, UserLogin, Token
from ..services.auth_service import AuthService
from ..utils.response import api_response

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

    user = auth_service.register_user(user_data)

    return api_response(
        status=True,
        message="User registered successfully",
        data=UserResponse.model_validate(user).model_dump()
    )


@router.post("/login")
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

    token_data = auth_service.authenticate_user(login_data)

    return api_response(
        status=True,
        message="Login successful",
        data=Token(**token_data).model_dump()
    )