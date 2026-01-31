import jwt

from typing import Annotated
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from .database import get_db
from .models import User


def get_current_user(
    db: Session = Depends(get_db), authorization: Annotated[str | None, Header()] = None
) -> User:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.partition(" ")[2]
    decoded_jwt = jwt.decode(token, "secret", algorithms="HS256")

    user_id = int(decoded_jwt["sub"])

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user
