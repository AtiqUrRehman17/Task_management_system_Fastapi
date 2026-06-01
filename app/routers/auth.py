from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.user import UserCreate, UserResponse, UserLogin, Token
from ..schemas.common import ResponseModel
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=ResponseModel[UserResponse])
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.register_user(user_data)
    
    return ResponseModel(
        success=True,
        message="User registered successfully",
        data=UserResponse.model_validate(user)
    )

@router.post("/login", response_model=ResponseModel[Token])
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    token_data = auth_service.authenticate_user(login_data)
    
    return ResponseModel(
        success=True,
        message="Login successful",
        data=Token(**token_data)
    )