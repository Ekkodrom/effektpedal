import logging
import os

class Logger:
    def __init__(self, log_file="logs/effect_pedal.log", level=logging.DEBUG):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        self.logger = logging.getLogger("EffectPedalLogger")
        self.logger.setLevel(level)
        
        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

if __name__ == "__main__":
    log = Logger()
    log.info("Logger initialized.")
    log.debug("This is a debug message.")
    log.warning("Warning: Something might be off.")
    log.error("Error: Something went wrong!")
    log.critical("Critical: System failure!")
