from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import User
from .models import Todo

from .schemas import UserCreate
from .schemas import TodoCreate, TodoUpdate

from .utils import hash_password

from .exceptions import TodoNotFound, EmailAlreadyRegistered, UserNotFound


def get_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)

    if not user:
        raise UserNotFound(user_id=user_id)

    return user


def create_user(db: Session, data: UserCreate) -> User:
    password = hash_password(data.password)

    user = User(**data.model_dump(exclude={"password"}), hashed_password=password)
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyRegistered(data.email)

    db.refresh(user)
    return user


def get_todo(db: Session, todo_id: int) -> Todo:
    todo = db.get(Todo, todo_id)

    if not todo:
        raise TodoNotFound(todo_id=todo_id)

    return todo


def create_todo(db: Session, data: TodoCreate, user_id: int) -> Todo:
    todo = Todo(**data.model_dump(), user_id=user_id)
    db.add(todo)

    db.commit()

    db.refresh(todo)
    return todo


def update_todo(db: Session, data: TodoUpdate, todo_id: int) -> Todo:
    todo = db.get(Todo, todo_id)

    if not todo:
        raise TodoNotFound(todo_id=todo_id)

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(todo, field, value)

    db.commit()

    db.refresh(todo)
    return todo


def get_user_by_email(db: Session, email: str) -> User:
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFound(email=email)

    return user
