from logging import handlers
import logging

class TRLog(object):
    def __init__(self, name, log_dir=None):
        self.log = logging.getLogger(name)

        if log_dir:
            self.setup_log(log_dir)
            
    def setup_log(self, log_path, level=logging.CRITICAL):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%H:%M:%S')
        handler = handlers.RotatingFileHandler(log_path, 'a', 500000, 10)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.log.logger.addHandler(handler)