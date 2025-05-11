import logging
from datetime import datetime

from fastapi import Request, FastAPI
from pydantic import ValidationError, BaseModel, Field
from starlette import status

from starlette.responses import JSONResponse

from logmaster.server.utils.exception import ResourceNotFoundException

_logger = logging.getLogger(__name__)


class ExceptionResponse(BaseModel):
    details: str = Field(description="Details message")
    exception_class: str = Field(description="Exception class name")
    timestamp: str = Field(description='Timestamp the error occurred', default=str(datetime.now()))

    @classmethod
    def from_exception(cls, e: BaseException):
        return cls(
            details=str(e),
            exception_class=e.__class__.__name__,
        )

    def to_json_response(self, status_code: int):
        return JSONResponse(
            content=self.model_dump(),
            status_code=status_code
        )


def _handler_method(fn):
    def wrapper(request: Request, exc: Exception):
        msg = f"Received request {request.method} {request.url} raised an exception: params[{request.query_params}]"
        _logger.exception(msg, exc_info=exc)
        return fn(request, exc)
    return wrapper


@_handler_method
def handle_not_found(_: Request, exc: Exception):
    return ExceptionResponse.from_exception(exc).to_json_response(status.HTTP_404_NOT_FOUND)


@_handler_method
def handle_bad_request(_: Request, exc: Exception):
    return ExceptionResponse.from_exception(exc).to_json_response(status.HTTP_400_BAD_REQUEST)


@_handler_method
def handle_generic_server_error(_: Request, exc: Exception):
    if isinstance(exc, ValidationError):
        # if pydantic validation fails, we assume that it's a bad request and not a bug (LOL)
        return ExceptionResponse.from_exception(exc).to_json_response(status.HTTP_400_BAD_REQUEST)
    return ExceptionResponse.from_exception(exc).to_json_response(status.HTTP_500_INTERNAL_SERVER_ERROR)


@_handler_method
def handle_forbidden(_: Request, exc: Exception):
    return ExceptionResponse.from_exception(exc).to_json_response(status.HTTP_403_FORBIDDEN)


@_handler_method
def handle_conflict(_: Request, exc: Exception):
    return ExceptionResponse.from_exception(exc).to_json_response(status.HTTP_409_CONFLICT)


_handlers = [
    {
        'exceptions': [ResourceNotFoundException],
        'handler': handle_not_found
    },
    {
        'exceptions': [],
        'handler': handle_bad_request
    },
    {
        'exceptions': [],
        'handler': handle_forbidden
    },
    {
        'exceptions': [],
        'handler': handle_conflict
    },
]


def register_handlers(app: FastAPI):
    app.add_exception_handler(500, handle_generic_server_error)
    for handler in _handlers:
        for e in handler['exceptions']:
            app.add_exception_handler(e, handler['handler'])
