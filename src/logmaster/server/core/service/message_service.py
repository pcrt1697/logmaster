import logging

from logmaster.core.producer.message import LogMessageProducerClient
from logmaster.server.core.models.document import Message
from logmaster.server.core.models.dto import MessageInput, MessagePageInput
from logmaster.server.core.models.page import MessagePage
from logmaster.server.core.models.resource import MessageResource
from logmaster.server.core.service.pagination import paginate

_logger = logging.getLogger(__name__)


async def produce_message(message_input: MessageInput):
    producer = LogMessageProducerClient()
    log_message = message_input.to_log_message()
    producer.produce(log_message)


async def search_messages(page: MessagePageInput):
    return await paginate(page, Message, MessagePage, MessageResource)
