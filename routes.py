from typing import Any

from fastapi import APIRouter

from .schemas import UserCreate
from .schemas import TodoCreate, TodoOut, TodoUpdate
from .schemas import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate) -> Any:
    pass


@router.post("/login", response_model=TokenResponse)
async def login(login_request: LoginRequest) -> Any:
    pass


@router.post("/todos", response_model=TodoOut)
async def create_todo(todo: TodoCreate) -> Any:
    pass


@router.put("/todos/{id}", response_model=TodoOut)
async def update_todo(data: TodoUpdate, id: int) -> Any:
    pass


@router.delete("/todos/{id}")
async def delete_todo(id: int) -> Any:
    pass


@router.get("/todos", response_model=list[TodoOut])
async def get_todos(page: int, limit: int) -> Any:
    pass
