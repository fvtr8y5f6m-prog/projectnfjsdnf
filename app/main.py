from fastapi import FastAPI
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "졸업프로젝트 IFF 백엔드 서버이다노"}