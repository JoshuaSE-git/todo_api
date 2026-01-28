import jwt

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from typing import Sequence

from .models import User
from .models import Todo

from .schemas import LoginRequest, UserCreate
from .schemas import TodoCreate, TodoUpdate

from .utils import hash_password, valid_password

from .exceptions import (
    InvalidCredentials,
    TodoNotFound,
    EmailAlreadyRegistered,
    UserNotFound,
    TodoForbidden,
)


def get_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)

    if not user:
        raise UserNotFound(user_id=user_id)

    return user


def create_user(db: Session, data: UserCreate) -> str:
    password = hash_password(data.password)

    user = User(**data.model_dump(exclude={"password"}), hashed_password=password)
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyRegistered(data.email)

    db.refresh(user)

    return jwt.encode({"sub": user.id, "type": "access"}, "secret", algorithm="HS256")


def get_todo(db: Session, todo_id: int) -> Todo:
    todo = db.get(Todo, todo_id)

    if not todo:
        raise TodoNotFound(todo_id=todo_id)

    return todo


def get_todos(
    db: Session, user: User, page: int, limit: int
) -> tuple[Sequence[Todo], int]:
    offset = (page - 1) * limit

    stmt = (
        select(Todo)
        .where(Todo.user_id == user.id)
        .order_by(Todo.id.asc())
        .limit(limit)
        .offset(offset)
    )

    todos = db.execute(stmt).scalars().all()
    total = db.query(Todo).filter(Todo.user_id == user.id).count()

    return todos, total


def create_todo(db: Session, data: TodoCreate, user: User) -> Todo:
    todo = Todo(**data.model_dump(), user_id=user.id)
    db.add(todo)

    db.commit()

    db.refresh(todo)
    return todo


def update_todo(db: Session, data: TodoUpdate, todo: Todo) -> Todo:
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(todo, field, value)

    db.commit()

    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: Todo) -> None:
    db.delete(todo)
    db.commit()


def get_user_by_email(db: Session, email: str) -> User:
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFound(email=email)

    return user


def login(db: Session, login_request: LoginRequest) -> str:
    try:
        user = get_user_by_email(db, login_request.email)
    except UserNotFound:
        raise InvalidCredentials

    if not valid_password(login_request.password, user.hashed_password):
        raise InvalidCredentials

    db.refresh(user)

    return jwt.encode({"sub": user.id, "type": "access"}, "secret", algorithm="HS256")


def assert_todo_access(user: User, todo: Todo):
    if user.id != todo.user_id:
        raise TodoForbidden(todo.id)
