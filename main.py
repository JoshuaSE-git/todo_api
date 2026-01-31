from fastapi import FastAPI
from . import models
from .database import Base, engine
from .routes import router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(router)


@app.get("/")
def index():
    return {"message": "hello"}
