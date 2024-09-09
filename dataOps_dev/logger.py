import os
import logging

class CustomLogger:
    def __init__(self, log_file='my_log.log', logger_name='my_logger', level=logging.DEBUG):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)

def setup_logger(log_file='my_log.log', logger_name='my_logger', level=logging.DEBUG):
    return CustomLogger(log_file, logger_name, level).logger
