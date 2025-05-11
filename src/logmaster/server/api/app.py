import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from uvicorn.config import LOGGING_CONFIG

from logmaster.server.api.exception_handler import register_handlers
from logmaster.server.api.v1.api import get_api as get_api_v1
from logmaster.server.core.mongodb import init_db


def get_logging_config():
    # TODO: integrate the following with the root logger of the application (e.g stream to file, etc..)
    for name, cfg in LOGGING_CONFIG['formatters'].items():
        cfg.pop('fmt', None)
        cfg.pop('use_colors', None)
        cfg['()'] = 'logmaster.server.utils.logging_manager.LogFormatter'
    return LOGGING_CONFIG


def register_api_version(main_app: FastAPI, child_app: FastAPI, path: str, name: str):
    register_handlers(child_app)
    main_app.mount(path, child_app, name=name)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore

    logger = logging.getLogger(__name__)

    await init_db()
    logger.info("Startup complete")
    yield
    logger.info("Shutdown complete")


def run_app(port: int = None, dev: bool = False):
    app = FastAPI(
        title="LogMaster backend APIs",
        version="1.0",
        summary="REST APIs to interact with LogMaster backend",
        root_path='/api',
        lifespan=lifespan
    )
    register_handlers(app)

    register_api_version(app, get_api_v1(dev), "/v1", "api-v1")

    uvicorn.run(app, host='0.0.0.0', port=port, root_path='', log_config=get_logging_config())
    # uvicorn.run(app, host='0.0.0.0', port=port, root_path='')
