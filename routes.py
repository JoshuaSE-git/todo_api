import services

from typing import Any, Annotated

from fastapi import APIRouter, Depends

from database import get_db

from sqlalchemy.orm import Session

from .dependencies import get_current_user

from .schemas import UserCreate
from .schemas import TodoCreate, TodoOut, TodoUpdate
from .schemas import LoginRequest, TokenResponse

from .models import User

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate, db: Annotated[Session, Depends(get_db)]) -> Any:
    return TokenResponse(token=services.create_user(db, data))


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> Any:
    return TokenResponse(token=services.login(db, data))


@router.post("/todos", response_model=TodoOut)
async def create_todo(
    data: TodoCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    todo = services.create_todo(db, data, user)

    return todo


@router.put("/todos/{id}", response_model=TodoOut)
async def update_todo(
    data: TodoUpdate,
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    todo = services.get_todo(db, todo_id)
    services.assert_todo_access(user, todo)
    todo = services.update_todo(db, data, todo)

    return todo


@router.delete("/todos/{id}", status_code=204)
async def delete_todo(
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    todo = services.get_todo(db, todo_id)
    services.assert_todo_access(user, todo)
    services.delete_todo(db, todo)


@router.get("/todos", response_model=list[TodoOut])
async def get_todos(
    page: int,
    limit: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    pass
