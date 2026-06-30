from fastapi import FastAPI
app = FastAPI(title="Industrial-knowledge-intelligence API",
description="Backend API for Industrial Knowledge Intelligence Platform",
version="0.1.0"

)

@app.get("/")
def home():
    return {"message":"Industrial-knowledge-intelligence API is running",
             "status":"success"}

