from typing import TYPE_CHECKING

from fastapi_mail import FastMail, MessageSchema, MessageType

from .schemas import EmailSchema

if TYPE_CHECKING:
    from fastapi_mail import ConnectionConfig


class SMTPService:
    def __init__(self, config: "ConnectionConfig"):
        self.fm = FastMail(config)

    @staticmethod
    def _create_message(subject: str, email_content: EmailSchema) -> MessageSchema:
        return MessageSchema(
            subject=subject,
            recipients=email_content.model_dump().get("email"),
            template_body=email_content.model_dump().get("body"),
            subtype=MessageType.html,
        )

    async def send_email(
        self,
        subject: str,
        email_content: EmailSchema,
        template_name: str,
    ):
        message = self._create_message(subject, email_content)

        await self.fm.send_message(message, template_name=template_name)
