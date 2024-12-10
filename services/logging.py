import logging
from rich.logging import RichHandler

def setup_logging(level=logging.ERROR):
    """
    :param level: Уровень логирования, по умолчанию WARNING.
    """
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    logger = logging.getLogger("AutoReactionBot")
    logger.setLevel(level)
    return logger
