from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import User
from .models import Todo

from .schemas import UserCreate
from .schemas import TodoCreate, TodoUpdate

from .utils import hash_password

from .exceptions import TodoNotFound, UserNotFound


def get_user(db_session: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFound(user_id=user_id)

    return user


def create_user(db_session: Session, data: UserCreate) -> User:
    password = hash_password(data.password)

    user = User(**data.model_dump(exclude={"password"}), password=password)
    db_session.add(user)

    db_session.commit()

    return user


def get_todo(db_session: Session, todo_id: int) -> Todo | None:
    stmt = select(Todo).where(Todo.id == todo_id)
    result = db_session.execute(stmt)
    todo = result.scalar_one_or_none()

    if not Todo:
        raise TodoNotFound(todo_id=todo_id)

    return todo


def create_todo(db_session: Session, data: TodoCreate, user_id: int) -> Todo:
    todo = Todo(**data.model_dump(), user_id=user_id)
    db_session.add(todo)

    db_session.commit()

    return todo


def update_todo(db_session: Session, data: TodoUpdate, todo_id: int) -> Todo:
    stmt = select(Todo).where(Todo.id == todo_id)
    todo = db_session.execute(stmt).scalar_one_or_none()

    if not todo:
        raise TodoNotFound(todo_id=todo_id)

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(todo, field, value)

    db_session.commit()
    db_session.refresh(todo)

    return todo


def get_user_by_email(db_session: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFound(email=email)

    return user
