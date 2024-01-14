from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./gwd.db" # "postgresql://localhost/gwd"
