import redis.asyncio
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    RedisStrategy,
)

from src.config import RedisConfig

redis_config = RedisConfig.from_env()
redis_url = redis_config.url
redis_client = redis.asyncio.from_url(redis_url, decode_responses=True)


def get_strategy() -> RedisStrategy:
    return RedisStrategy(redis_client, lifetime_seconds=3600)


def get_auth_backend() -> AuthenticationBackend:
    cookie_transport = CookieTransport(cookie_max_age=3600)
    return AuthenticationBackend(
        name="cookie",
        transport=cookie_transport,
        get_strategy=get_strategy,
    )
