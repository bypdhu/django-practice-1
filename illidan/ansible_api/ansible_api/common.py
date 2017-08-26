import logging

log = logging.getLogger("ansible_api")


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


log.addHandler(NullHandler)
