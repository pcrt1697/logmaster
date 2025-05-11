from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from logmaster.server.core.models.document import DOCUMENT_MODELS
from logmaster.core.config import EnvVars


async def init_db(connection_string: str = None):
    if connection_string is None:
        connection_string = EnvVars.DB_URL.get_value()
    client = AsyncIOMotorClient(connection_string)
    await init_beanie(database=client.get_database("logmaster"), document_models=list(DOCUMENT_MODELS))
