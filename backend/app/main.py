from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_db_and_tables

app = FastAPI(title=settings.PROJECT_NAME)


origins = [
   "http://localhost:5173"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
  create_db_and_tables()


@app.get("/")
def read_root():
  return {"Message": "Welcome to the {settings.PROJECT_NAME}"}