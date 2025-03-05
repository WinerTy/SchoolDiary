from pathlib import Path
from typing import List

from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from pydantic import BaseModel, EmailStr

from core.config import config


class EmailSchema(BaseModel):
    email: List[EmailStr]


# Этот класс от BaseSettings, переписать в наследование в конфиге! TODO
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


def send_email_via_html(email: EmailSchema, template_name: str):
    message = MessageSchema()


async def send_test_email(email: EmailSchema):
    # send_email_via_html(email, "email.html")
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.model_dump().get("email"),
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
