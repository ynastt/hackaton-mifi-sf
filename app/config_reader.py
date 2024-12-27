from os import PathLike
from pathlib import Path
from typing import Optional, Any

from pydantic import SecretStr, PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR_FOR_ENV = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr

    """DATABASE CONFIG"""
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_URL: str | None = None

    @field_validator("DB_URL")
    @classmethod
    def assemble_db_url(cls, v: Optional[PostgresDsn], info: FieldValidationInfo) -> Any:
        return v or (f"postgresql+asyncpg://{info.data.get('POSTGRES_USER')}:"
                     f"{info.data.get('POSTGRES_PASSWORD')}@{info.data.get('POSTGRES_SERVER')}:"
                     f"{info.data.get('POSTGRES_PORT')}/{info.data.get('POSTGRES_DB')}")


    """RABBITMQ CONFIG"""
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_LOGIN: str
    RABBITMQ_PASSWORD: str
    ARMQ_URL: str | None = None

    @field_validator("ARMQ_URL")
    @classmethod
    def assemble_armq_url(cls, v: Optional[str], info: FieldValidationInfo):
        if isinstance(v, str):
            print(v)
            return v

        host = info.data.get("RABBITMQ_HOST")
        port = info.data.get("RABBITMQ_PORT")
        login = info.data.get("RABBITMQ_LOGIN")
        password = info.data.get("RABBITMQ_PASSWORD")

        if all([host, port, login, password]):
            return f"amqp://{login}:{password}@{host}:{port}"
        else:
            return None

    CV_QUEUE_NAME: str
    NLP_QUEUE_NAME: str

    # ML MODEL CONFIG
    NLP_MODEL_PATH: str | PathLike = BASE_DIR_FOR_ENV / 'app/app/models/rubert-tiny-sentiment-balanced.onnx'
    TOKENIZER_DIR_NAME: str | PathLike = BASE_DIR_FOR_ENV / 'app/app/tokenizers/sent_tokenizer'
    YOLO_MODEL_PATH: str | PathLike = BASE_DIR_FOR_ENV / 'app/app/models/best.pt'

    model_config = SettingsConfigDict(env_file=BASE_DIR_FOR_ENV / '.env', env_file_encoding='utf-8', extra='allow')


# При импорте файла сразу создастся 
# и провалидируется объект конфига, 
# который можно далее импортировать из разных мест
config = Settings()
