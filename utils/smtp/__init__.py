from pathlib import Path

from fastapi_mail import ConnectionConfig

from core.config import config

conf = ConnectionConfig(
    MAIL_USERNAME=config.smtp.mail_username,
    MAIL_PASSWORD=config.smtp.mail_password,
    MAIL_FROM=str(config.smtp.mail_from),
    MAIL_PORT=config.smtp.mail_port,
    MAIL_SERVER=config.smtp.mail_server,
    MAIL_FROM_NAME=config.smtp.mail_from_name,
    MAIL_STARTTLS=config.smtp.mail_starttls,
    MAIL_SSL_TLS=config.smtp.mail_ssl_tls,
    USE_CREDENTIALS=config.smtp.use_credentials,
    VALIDATE_CERTS=config.smtp.validate_certs,
    TEMPLATE_FOLDER=Path(__file__).parent.parent.parent / "templates",
)
