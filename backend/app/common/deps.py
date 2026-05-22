from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.security.jwt import decode_access_token
from app.common.exceptions import UnauthorizedError, TokenInvalidError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    if token is None:
        raise UnauthorizedError()
    payload = decode_access_token(token)
    if payload is None:
        raise TokenInvalidError()
    user_id: int = payload.get("sub")
    if user_id is None:
        raise TokenInvalidError()

    from app.modules.auth.models import User

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise TokenInvalidError("用户不存在")
    return user


__all__ = ["get_db", "get_current_user"]
