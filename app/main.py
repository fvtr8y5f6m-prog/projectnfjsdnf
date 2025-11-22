from fastapi import FastAPI, UploadFile, File
from .database import engine
from . import models, ai_core
import shutil
import os

# DB 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 임시 저장소 설정
UPLOAD_DIR = "temp_uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def read_root():
    return {"message": "졸업프로젝트 IFF 백엔드 서버이다노"}

@app.post("/api/analyze")
async def analyze_voice(file: UploadFile = File(...)):
    # 1. 파일명 확인 및 저장 경로 설정
    save_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = ai_core.analyze_audio_with_google(save_path)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)

    return result