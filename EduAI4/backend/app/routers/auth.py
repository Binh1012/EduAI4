from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import current_user
from ..models import User
from ..schemas import LoginIn, RegisterIn, TokenOut
from ..security import create_token, hash_password, verify_password

router = APIRouter(tags=["auth"])


@router.post("/auth/register", response_model=TokenOut, status_code=201)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    email = body.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "Email này đã được đăng ký")
    # Role is always STUDENT here; teachers/admins are created by an admin.
    user = User(email=email, name=body.name.strip(), password_hash=hash_password(body.password), role="STUDENT")
    db.add(user)
    db.commit()
    return TokenOut(access_token=create_token(user.id, user.role), name=user.name, role=user.role)


@router.post("/auth/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.lower()).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Sai email hoặc mật khẩu")
    return TokenOut(access_token=create_token(user.id, user.role), name=user.name, role=user.role)


@router.get("/me")
def me(user: User = Depends(current_user)):
    return {"id": user.id, "email": user.email, "name": user.name, "role": user.role}
