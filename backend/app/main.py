from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.routes.main_router import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    create_db_and_tables()
    yield
  
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(GZipMiddleware, minimum_size=1000)

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

app.include_router(main_router)


@app.get("/")
def read_root():
    return {"Message": f"Welcome to the {settings.PROJECT_NAME}"}