from dishka import make_async_container
from dishka.integrations import fastapi as fastapi_integration
from dishka.integrations import faststream as faststream_integration
from fastapi import FastAPI
from faststream import FastStream
from faststream.broker.core.usecase import BrokerUsecase

from src.config import Config
from src.controllers.ampq.router import ampq_router
from src.controllers.api.router import router as api_router
from src.infrastructure.broker.connection import new_broker
from src.ioc import AppProvider

config = Config.from_env()
broker = new_broker(config.rabbitmq)
container = make_async_container(
    AppProvider(),
    context={Config: config, BrokerUsecase: broker},
)


def get_faststream_app() -> FastStream:
    faststream_app = FastStream(broker)
    faststream_integration.setup_dishka(container, faststream_app, auto_inject=True)
    broker.include_router(ampq_router)
    return faststream_app


def get_fastapi_app():
    app = FastAPI()
    app.include_router(api_router)
    fastapi_integration.setup_dishka(container, app)

    return app


def get_app():
    fastapi_app = get_fastapi_app()
    faststream_app = get_faststream_app()
    fastapi_app.add_event_handler('startup', faststream_app.start)
    fastapi_app.add_event_handler('shutdown', faststream_app.stop)
    return fastapi_app
