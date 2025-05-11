from logmaster.server.core.models.document import App
from logmaster.server.core.models.dto import AppInput, AppPageInput
from logmaster.server.core.models.page import AppPage
from logmaster.server.core.models.resource import AppResource
from logmaster.server.core.service.pagination import paginate
from logmaster.server.utils.exception import ResourceNotFoundException


async def create_app(id_app: str, app_input: AppInput):
    app = app_input.to_document(id_app)
    await app.save()
    return app


async def get_app_by_id(id_app: str):
    app = await App.get(id_app)
    if app is None:
        raise ResourceNotFoundException.by_id(App, id_app)
    return app


async def delete_app_by_id(id_app: str):
    app = await App.get(id_app)
    if app is None:
        raise ResourceNotFoundException.by_id(App, id_app)
    await app.delete()
    return app


async def get_app_page(page: AppPageInput):
    return await paginate(page, App, AppPage, AppResource)
