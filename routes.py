import services

from typing import Any, Annotated

from fastapi import APIRouter, Depends, Query

from database import get_db

from sqlalchemy.orm import Session

from .dependencies import get_current_user

from .schemas import PaginatedTodoResponse, UserCreate
from .schemas import TodoCreate, TodoOut, TodoUpdate
from .schemas import LoginRequest, TokenResponse

from .models import User

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate, db: Annotated[Session, Depends(get_db)]) -> Any:
    return services.create_user(db, data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> Any:
    return services.login(db, data)


@router.post("/todos", response_model=TodoOut)
async def create_todo(
    data: TodoCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    return services.create_todo(db, data, user)


@router.put("/todos/{id}", response_model=TodoOut)
async def update_todo(
    data: TodoUpdate,
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    todo = services.get_todo(db, todo_id)
    services.assert_todo_access(user, todo)

    return services.update_todo(db, data, todo)


@router.delete("/todos/{id}", status_code=204)
async def delete_todo(
    todo_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    todo = services.get_todo(db, todo_id)
    services.assert_todo_access(user, todo)
    services.delete_todo(db, todo)


@router.get("/todos", response_model=PaginatedTodoResponse)
async def get_todos(
    page: Annotated[int, Query(ge=1, default=1)],
    limit: Annotated[int, Query(ge=1, le=100, default=10)],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Any:
    todos, total = services.get_todos(db, user, page, limit)

    return {"data": todos, "page": page, "limit": limit, "total": total}
