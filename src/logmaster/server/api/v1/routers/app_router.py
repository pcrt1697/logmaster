from typing import Annotated

from fastapi import APIRouter, Path, Body

from logmaster.server.core.models.dto import AppInput, AppPageInput
from logmaster.server.core.models.page import AppPage
from logmaster.server.core.models.resource import AppResource
from logmaster.server.core.service import app_service

app_router = APIRouter(prefix="/apps", tags=["apps"])


@app_router.put("/{id_app}", response_model=AppResource)
async def upsert_app(
        id_app: Annotated[str, Path(description='App identifier')],
        app_input: Annotated[AppInput, Body(description='Application data')],
):
    app = await app_service.create_app(id_app, app_input)
    return AppResource.from_model(app)


@app_router.get("/{id_app}", response_model=AppResource)
async def get_app(
        id_app: Annotated[str, Path(description='App identifier')],
):
    app = await app_service.get_app_by_id(id_app)
    return AppResource.from_model(app)


@app_router.delete(
    "/{id_app}",
    response_model=AppResource
)
async def delete_app(
        id_app: Annotated[str, Path(description='App identifier')],
):
    app = await app_service.delete_app_by_id(id_app)
    return AppResource.from_model(app)


@app_router.post("/_search", response_model=AppPage)
async def get_app_page(
        app_page: Annotated[AppPageInput, Body(description='Application page query')],
):
    return await app_service.get_app_page(app_page)
