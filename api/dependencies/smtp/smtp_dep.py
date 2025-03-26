import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from fastapi_mail import ConnectionConfig

from core.config import config
from smtp.service import SMTPService


async def get_configuration() -> ConnectionConfig:
    template_folder = Path(__file__).parent.parent.parent.parent / "templates/email"
    os.makedirs(template_folder, exist_ok=True)
    yield ConnectionConfig(
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
        TEMPLATE_FOLDER=template_folder,
    )


async def get_smtp_service(
    config: Annotated[ConnectionConfig, Depends(get_configuration)],
) -> SMTPService:
    yield SMTPService(config=config)
