from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .database import Base, engine
from .routes import router
from .exceptions import (
    TodoForbidden,
    InvalidCredentials,
    TodoNotFound,
    UserNotFound,
    EmailAlreadyRegistered,
)

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router)


@app.exception_handler(TodoNotFound)
def todo_not_found_handler(request: Request, exc: TodoNotFound):
    return JSONResponse(status_code=401, content={"message": "todo not found"})


@app.exception_handler(TodoForbidden)
def todo_forbidden_handler(request: Request, exc: TodoForbidden):
    return JSONResponse(status_code=403, content={"message": "forbidden"})


@app.exception_handler(InvalidCredentials)
def invalid_credentials_handler(request: Request, exc: InvalidCredentials):
    return JSONResponse(
        status_code=401, content={"message": "invalid email or password"}
    )


@app.exception_handler(UserNotFound)
def user_not_found_handler(reqeust: Request, exc: UserNotFound):
    return JSONResponse(status_code=401, content={"message", "user not found"})


@app.exception_handler(EmailAlreadyRegistered)
def email_already_registered_handler(reqeust: Request, exc: EmailAlreadyRegistered):
    return JSONResponse(
        status_code=401, content={"message": "email already registered"}
    )
