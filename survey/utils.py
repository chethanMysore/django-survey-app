from enum import Enum
import logging


class Logger:
    def __init__(self, model_name, logger_path):
        self.logger = logging.getLogger(model_name)
        hdlr = logging.FileHandler(logger_path)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def get_logger(self):
        return self.logger


class FeedbackType(Enum):
    Query: 1
    Suggestion: 2
    Complaint: 3
