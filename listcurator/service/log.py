import logging, sys
from logging import CRITICAL, WARNING, ERROR, DEBUG, INFO


LOGGER_NAME = "ListCuratorLogger"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = DEBUG


class Logger(object):
    def __init__(self, logger_name=LOGGER_NAME, log_level=LOG_LEVEL, log_fmt=LOG_FORMAT, create_console=True, log_file=None):
        self.log_level = log_level
        self.logger_name = logger_name
        self.logger = self.setup_logging(logger_name, log_level, create_console, log_file, log_fmt)


    def setup_logging(self, logger_name, log_level, create_console, log_file, log_fmt):

        if log_file:
            self.setup_logging_file(logger_name, log_level, log_fmt, log_file)
        if create_console:
            self.setup_logging_console(logger_name, log_level, log_fmt)
        return logging.getLogger(logger_name)

    def setup_logging_console(self, logger_name, log_level, log_fmt):
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(log_fmt)
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
        logger.setLevel(log_level)
        return logger

    def setup_logging_file(self, logger_name, log_level, log_fmt, log_file):
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(log_fmt)
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)
        logger.setLevel(log_level)
        return logger

    def log_format(self, msg, **kargs):
        self.logger.log(self.log_level, msg.format(**kargs))

    def critical(self, msg, **kargs):
        self.logger.critical(msg.format(**kargs))

    def warning(self, msg, **kargs):
        self.logger.warning(msg.format(**kargs))

    def error(self, msg, **kargs):
        self.logger.error(msg.format(**kargs))

    def debug(self, msg, **kargs):
        self.logger.debug(msg.format(**kargs))

    def info(self, msg, **kargs):
        self.logger.info(msg.format(**kargs))

