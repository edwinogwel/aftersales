from fastapi import FastAPI
from . import models
from .database import engine
from .routers import service_job, service_request

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(service_job.router)
app.include_router(service_request.router)


@app.get("/")
def index():
    return {"message": "Hello World!"}
