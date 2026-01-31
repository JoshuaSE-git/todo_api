from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    todos: Mapped[list["Todo"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, hashed_password={self.hashed_password!r})"


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    user_id = mapped_column(ForeignKey("user.id"))

    user: Mapped[User] = relationship(back_populates="todos")

    def __repr__(self) -> str:
        return f"Todo(id={self.id!r}, title={self.title!r}, description={self.description!r})"
