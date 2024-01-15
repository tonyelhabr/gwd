from typing import Any, Dict, Optional

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    ## https://stackoverflow.com/questions/77134535/migrate-postgresdsn-build-from-pydentic-v1-to-pydantic-v2
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            ## don't need any extra forward-slash before the db
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        ).unicode_string()

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
