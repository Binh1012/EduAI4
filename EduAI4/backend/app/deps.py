from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .security import decode_token

bearer = HTTPBearer(auto_error=False)


def current_user(cred: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if cred is None:
        raise HTTPException(401, "Cần đăng nhập")
    try:
        uid = int(decode_token(cred.credentials)["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(401, "Phiên đăng nhập đã hết hạn")
    user = db.get(User, uid)
    if not user:
        raise HTTPException(401, "Tài khoản không tồn tại")
    return user


def require_role(*roles: str):
    """Use for teacher/admin endpoints (Phase 4)."""
    def checker(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "Bạn không có quyền thực hiện thao tác này")
        return user
    return checker
