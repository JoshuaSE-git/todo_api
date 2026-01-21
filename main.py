from fastapi import FastAPI
from .routes import router


app = FastAPI()

app.include_router(router)


@app.get("/")
def index():
    return {"message": "hello"}
