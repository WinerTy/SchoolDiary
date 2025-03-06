from fastapi_mail import MessageSchema, MessageType, FastMail

from . import conf
from .schemas import EmailSchema


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
