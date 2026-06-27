from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.auth import create_access_token, get_password_hash, verify_password, get_current_user, oauth2_scheme
from app.schemas.auth import RegisterRequest, LoginRequest, Token, AuthResponse

auth_router = APIRouter()


@auth_router.post("/auth/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    from app.models.users import Users

    existing_user = db.query(Users).filter(Users.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = get_password_hash(payload.password)
    user = Users(
        email=payload.email,
        password_hash=hashed_password,
        display_name=payload.display_name,
        role=payload.role or "player",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@auth_router.post("/auth/login", response_model=Token)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    from app.models.users import Users

    user = db.query(Users).filter(Users.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(
        access_token=access_token,
        user_id=user.id,
        email=user.email,
        display_name=user.display_name,
    )


@auth_router.get("/auth/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "display_name": current_user.display_name,
        "role": current_user.role,
    }
