from fastapi_users.authentication import BearerTransport

from core.config import config

bearer_transport = BearerTransport(
    tokenUrl=config.api.auth.token_url,
)
