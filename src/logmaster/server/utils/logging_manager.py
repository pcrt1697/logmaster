import logging

from logmaster.core.logging import LogFormatter, LINE_FORMAT


def remove_handlers(logger: logging.Logger):
    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.close()


def configure_logging(log_file: str = None, debug: bool = False):

    logger = logging.getLogger()
    remove_handlers(logger)
    if debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy').setLevel(logging.INFO)
    else:
        logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(LogFormatter())
    logger.addHandler(stream_handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setFormatter(logging.Formatter(LINE_FORMAT))
        logger.addHandler(file_handler)
