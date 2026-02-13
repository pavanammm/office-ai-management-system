from dotenv import load_dotenv
import os
from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import router

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Office AI System is running"}
print("DEBUG PORT VALUE:", os.environ.get("PORT"))


import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
