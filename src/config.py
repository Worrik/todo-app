from typing import Self

from environs import Env
from pydantic import BaseModel, Field


class RabbitMQConfig(BaseModel):
    host: str = Field(alias="RABBITMQ_HOST")
    port: int = Field(alias="RABBITMQ_PORT")
    login: str = Field(alias="RABBITMQ_USER")
    password: str = Field(alias="RABBITMQ_PASS")

    @classmethod
    def from_env(cls) -> Self:
        env = Env()
        env.read_env()
        return cls(
            RABBITMQ_HOST=env("RABBITMQ_HOST"),
            RABBITMQ_PORT=env.int("RABBITMQ_PORT"),
            RABBITMQ_USER=env("RABBITMQ_USER"),
            RABBITMQ_PASS=env("RABBITMQ_PASS"),
        )


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @classmethod
    def from_env(cls) -> Self:
        env = Env()
        env.read_env()
        return cls(
            POSTGRES_HOST=env("POSTGRES_HOST"),
            POSTGRES_PORT=env.int("POSTGRES_PORT"),
            POSTGRES_USER=env("POSTGRES_USER"),
            POSTGRES_PASSWORD=env("POSTGRES_PASSWORD"),
            POSTGRES_DB=env("POSTGRES_DB"),
        )


class RedisConfig(BaseModel):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")

    @classmethod
    def from_env(cls) -> Self:
        env = Env()
        env.read_env()
        return cls(
            REDIS_HOST=env("REDIS_HOST"),
            REDIS_PORT=env.int("REDIS_PORT"),
        )

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}"


class Config(BaseModel):
    rabbitmq: RabbitMQConfig = Field()
    postgres: PostgresConfig = Field()
    redis: RedisConfig = Field()

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            rabbitmq=RabbitMQConfig.from_env(),
            postgres=PostgresConfig.from_env(),
            redis=RedisConfig.from_env(),
        )
