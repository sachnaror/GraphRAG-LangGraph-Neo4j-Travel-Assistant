import sys
import logging

try:
    from loguru import logger as loguru_logger
except ModuleNotFoundError:
    loguru_logger = None


def configure_logger(level: str = "INFO"):
    if loguru_logger:
        loguru_logger.remove()
        loguru_logger.add(
            sys.stderr,
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
        )
        return loguru_logger

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    return logging.getLogger("travel-assistant")


app_logger = configure_logger()
