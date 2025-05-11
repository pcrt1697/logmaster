from typing import Annotated

from fastapi import APIRouter, Body
from starlette.status import HTTP_202_ACCEPTED

from logmaster.server.core.models.dto import MessageInput, MessagePageInput
from logmaster.server.core.models.page import MessagePage
from logmaster.server.core.service import message_service


def get_message_router(include_producer: bool):
    message_router = APIRouter(prefix="/messages", tags=["messages"])
    message_router.add_api_route(
        "/_search",
        search_messages,
        methods=["POST"],
        response_model=MessagePage,
        status_code=HTTP_202_ACCEPTED
    )
    if include_producer:
        message_router.add_api_route(
            "/producer",
            produce_message,
            methods=["POST"],
            response_model=MessageInput,
            status_code=HTTP_202_ACCEPTED
        )
    return message_router


async def search_messages(
        page_input: Annotated[MessagePageInput, Body(description='Message page')],
):
    return await message_service.search_messages(page_input)


async def produce_message(
        message_input: Annotated[MessageInput, Body(description='Message data')],
):
    await message_service.produce_message(message_input)
    return message_input
