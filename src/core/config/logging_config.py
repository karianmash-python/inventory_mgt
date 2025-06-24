import logging
from colorlog import ColoredFormatter
import os


def setup_logging():
    # Get log level from the environment or default to INFO
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Create a handler that outputs logs to the console
    handler = logging.StreamHandler()
    handler.setLevel(log_level)  # Capture all logs at the INFO level and above

    # Define a colored formatter for pretty console output
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            # Log Levels and their respective terminal colors
            'DEBUG': 'cyan',  # Developer-focused information (e.g., internal state, flow)
            'INFO': 'green',  # General runtime events (e.g., startup, user login)
            'WARNING': 'yellow',  # Something unexpected, but the app is still running fine
            'ERROR': 'red',  # Errors that caused a failure in a part of the app
            'CRITICAL': 'bold_red',  # Severe errors — application may crash or become unusable
        }
    )

    # Set the formatter to the handler
    handler.setFormatter(formatter)

    # Get the root logger (applies globally)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers to prevent duplicate log lines
    root_logger.handlers.clear()

    # Attach the color-enabled handler
    root_logger.addHandler(handler)

# Set the minimum level for the handler:
# logging.DEBUG    - Most verbose, used for development (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# logging.INFO     - General info (e.g., app started, user logged in) (INFO, WARNING, ERROR, CRITICAL)
# logging.WARNING  - Something unexpected but not breaking (WARNING, ERROR, CRITICAL)
# logging.ERROR    - An error occurred, app continues running (ERROR, CRITICAL)
# logging.CRITICAL - Severe error, app may crash (CRITICAL)
