from pydantic_settings import BaseSettings

class Settings(BaseSettings): 

    DATABASE_URL: str
    NASA_MAP_KEY: str
    PROJECT_NAME: str = "Wildfire Intelligence Engine"
    SECRET_KEY: str



    # Docker/Postgres Specifies
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    DB_NAME: str

    # Google Auth
    GOOGLE_CLIENT_ID: str
    CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str


    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()