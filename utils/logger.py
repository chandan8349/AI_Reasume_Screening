import logging
from config import config

def setup_logging():
    """
    Configures and returns a logger instance named 'AIResumeScreening'.
    
    This logger is set up with both a console (stream) handler and a file handler.
    The logging level is taken from the configuration. If the provided log level
    is invalid, it defaults to INFO.
    """
    # Convert the string log level from config to a numeric value
    numeric_level = getattr(logging, config.LOG_LEVEL.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO

    # Create a logger with a custom name
    logger = logging.getLogger("AIResumeScreening")
    logger.setLevel(numeric_level)
    logger.propagate = False  # Prevent logging messages from being propagated to the root logger

    # Create a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Set up stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(numeric_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Set up file handler to save logs to a file
    file_handler = logging.FileHandler("ai_resume_screening.log")
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# If this module is run directly, set up the logger and log a test message.
if __name__ == "__main__":
    log = setup_logging()
    log.info("Logger is configured and running.")
