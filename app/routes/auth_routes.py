from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.utils.auth import create_access_token, get_password_hash, verify_password
from app.schemas.auth import RegisterRequest, LoginRequest, Token

auth_router = APIRouter()

@auth_router.post("/auth/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(user_in: RegisterRequest, db: Session = Depends(get_db)):
    # Lazy import to avoid duplicate table registration
    from app.models.users import User

    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        password_hash=hashed_password,
        display_name=user_in.display_name,
        role=user_in.role,
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    access_token = create_access_token(data={"sub": new_user.email})
    return Token(access_token=access_token)

@auth_router.post("/auth/login", response_model=Token)
def login(login_in: LoginRequest, db: Session = Depends(get_db)):
    from app.models.users import User

    user = db.query(User).filter(User.email == login_in.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(login_in.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)
