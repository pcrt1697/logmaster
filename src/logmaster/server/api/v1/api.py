from fastapi import FastAPI

from logmaster.server.api.v1.routers.message_router import get_message_router
from logmaster.server.api.v1.routers.app_router import app_router


def get_api(dev: bool = False):
    metadata = []  # {'name': '', 'description': ''}
    api = FastAPI(
        title="LogMaster backend APIs",
        version='1.0',
        summary="REST APIs to interact with LogMaster backend",
        openapi_tags=metadata,
    )
    api.include_router(app_router)
    message_router = get_message_router(dev)
    api.include_router(message_router)
    return api
