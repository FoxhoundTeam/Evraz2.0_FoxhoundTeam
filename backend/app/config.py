from typing import Any, Dict, Optional

from pydantic import BaseSettings, MongoDsn, validator


class Settings(BaseSettings):
    project_name: str = "FoxControl"

    max_history_delta: int = 2 * 60 * 60  # 2 hours

    kafka_server: str = "rc1a-b5e65f36lm3an1d5.mdb.yandexcloud.net:9091"
    kafka_topic: str = "zsmk-9433-dev-01"
    kafka_user: str = "9433_reader"
    kafka_password: str

    mongodb_server: str = "db"
    mongodb_db: str = "controller"
    database_uri: Optional[MongoDsn] = None

    @validator("database_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return MongoDsn.build(
            scheme="mongodb",
            host=values.get("mongodb_server"),
            path=f"/{values.get('mongodb_db') or ''}",
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
