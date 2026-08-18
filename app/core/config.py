import logging
from pathlib import Path
from typing import Literal
from urllib.parse import quote

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s] #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s"
)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class LoggingConfig(BaseModel):
    log_level: Literal["debug", "info", "warning", "error", "critical"] = "info"
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


class PostgresqlConfig(SettingsBase):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    def _build_url(self, driver: str) -> str:
        user = quote(self.postgres_user, safe="")
        password = quote(self.postgres_password, safe="")
        db_name = quote(self.postgres_db, safe="")

        return (
            f"postgresql+{driver}://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{db_name}"
        )

    @property
    def database_url_asyncpg(self) -> str:
        return self._build_url("asyncpg")

    @property
    def database_url_psycopg(self) -> str:
        return self._build_url("psycopg")


class DatabaseConfig(BaseModel):
    postgresql: PostgresqlConfig = Field(default_factory=PostgresqlConfig)


class RedisConfig(SettingsBase):
    redis_host: str
    redis_port: int
    redis_user: str | None = "default"
    redis_password: str | None = None
    redis_db: int = 0

    def _build_url(self) -> str:
        host = self.redis_host
        port = self.redis_port
        db = self.redis_db

        if not self.redis_password:
            return f"redis://{host}:{port}/{db}"

        password = quote(self.redis_password, safe="")

        if self.redis_user:
            user = quote(self.redis_user, safe="")
            return f"redis://{user}:{password}@{host}:{port}/{db}"

        return f"redis://:{password}@{host}:{port}/{db}"

    @property
    def redis_url(self) -> str:
        return self._build_url()


class BrokerConfig(BaseModel):
    redis: RedisConfig = Field(default_factory=RedisConfig)


class CORSConfig(SettingsBase):
    cors_allow_origins: list[str]
    cors_allow_credentials: bool
    cors_allow_methods: list[str]
    cors_allow_headers: list[str]


class ProjectConfig(SettingsBase):
    project_title: str
    project_description: str


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    tender: str = "/tender"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Config = Field(default_factory=ApiV1Config)


class RunConfig(SettingsBase):
    run_host: str
    run_port: int
    debug: bool = True


class Config(BaseModel):
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    broker: BrokerConfig = Field(default_factory=BrokerConfig)
    cors: CORSConfig = Field(default_factory=CORSConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    run: RunConfig = Field(default_factory=RunConfig)


config = Config()
