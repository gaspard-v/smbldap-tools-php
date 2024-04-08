import logging
from logging import Logger as OrigLogger
from .singleton import SingletonMeta


class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        # syslog_handler = SysLogHandler(
        #     facility=SysLogHandler.LOG_DAEMON,
        #     address='/dev/log'
        # )
        formatter = logging.Formatter("%(module)s: %(levelname)s %(message)s")
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)


def log() -> OrigLogger:
    logger = Logger()
    return logger.logger
