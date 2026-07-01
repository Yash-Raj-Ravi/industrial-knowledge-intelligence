from fastapi import FastAPI,UploadFile,File,HTTPException
import os
import shutil
from .config import ALLOWED_TYPES, UPLOAD_DIR

app = FastAPI(title="Industrial Knowledge Intelligence API",
description="Backend API for Industrial Knowledge Intelligence Platform",
version="0.2.0")

@app.get("/")
def home():
    return {"message":"Industrial-knowledge-intelligence API is running",
             "status":"success"}

os.makedirs(UPLOAD_DIR,exist_ok=True)
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    file_path = os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path,"wb") as destination:
     shutil.copyfileobj(file.file,destination)
    return {"message":"File is uploaded successfully",
             "file_name":file.filename,
             "content_type":file.content_type,
             "path":file_path}



