from dotenv import load_dotenv
import os
from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import router
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Office AI System is running"}
print("DEBUG PORT VALUE:", os.environ.get("PORT"))



