from pydantic_settings import BaseSettings

class Settings(BaseSettings): 

    DATABASE_URL: str
    NASA_API_KEY: str
    PROJECT_NAME: str = "Wildfire Intelligence Engine"
    SECRET_KEY: str



    # Docker/Postgres Specifies
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    DB_NAME: str


    class Config:
        env_file = ".env"

settings = Settings()