import secrets

from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn, RedisDsn, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class SmtpSettings(BaseModel):
    mail_username: str
    mail_password: str
    mail_from: EmailStr
    mail_port: int = 465
    mail_server: str = "smtp.yandex.ru"
    mail_from_name: str = "School Management System"
    mail_starttls: bool = True
    mail_ssl_tls: bool = True
    use_credentials: bool = True
    validate_certs: bool = True


class RedisSettings(BaseModel):
    url: RedisDsn


class ApiAuth(BaseModel):
    token_url: str = "api/auth/login"


class ApiSettings(BaseModel):
    auth: ApiAuth = ApiAuth()


class AuthSettings(BaseModel):
    secret: str = secrets.token_hex()
    life_time: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class ServerSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8001      
    debug: bool = True


class DataBaseSettings(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AppSettings(BaseSettings):
    smtp: SmtpSettings
    api: ApiSettings = ApiSettings()
    auth: AuthSettings
    server: ServerSettings = ServerSettings()
    db: DataBaseSettings
    redis: RedisSettings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


config = AppSettings()
