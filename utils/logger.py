import logging
import os
import sys
import inspect
import multiprocessing
from pathlib import Path


class Logger:
    """
    A custom logger that displays process name, file path, line number, and message.

    Attributes:
        logger (logging.Logger): The underlying logger instance
        level (int): The logging level
        format_string (str): The format string for log messages
    """

    def __init__(self, name=None, level=logging.INFO, output_file=None):
        """
        Initialize the custom logger.

        Args:
            name (str, optional): Logger name. Defaults to the calling module's name.
            level (int, optional): Logging level. Defaults to logging.INFO.
            output_file (str, optional): Path to log file. If provided, logs will be written to this file.
        """
        # Get the name of the calling module if not provided
        if name is None:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            name = module.__name__ if module else "unknown_module"

        self.logger = logging.getLogger(name)
        self.level = level
        self.logger.setLevel(level)

        # Create a formatter that includes process name, file path, line number, and message
        self.format_string = "[%(pathname)s:%(lineno)d] %(levelname)s: %(message)s"
        formatter = logging.Formatter(self.format_string)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create file handler if output_file is provided
        if output_file:
            file_handler = logging.FileHandler(output_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        """Log a debug message."""
        # Get the caller's filename and line number
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno

        # Create a LogRecord with the caller's information
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.DEBUG,
            pathname=filename,
            lineno=lineno,
            msg=message,
            args=(),
            exc_info=None,
        )

        # Set the process name
        record.processName = multiprocessing.current_process().name

        self.logger.handle(record)

    def info(self, message):
        """Log an info message."""
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno

        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.INFO,
            pathname=filename,
            lineno=lineno,
            msg=message,
            args=(),
            exc_info=None,
        )

        record.processName = multiprocessing.current_process().name

        self.logger.handle(record)

    def warning(self, message):
        """Log a warning message."""
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno

        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.WARNING,
            pathname=filename,
            lineno=lineno,
            msg=message,
            args=(),
            exc_info=None,
        )

        record.processName = multiprocessing.current_process().name

        self.logger.handle(record)

    def error(self, message):
        """Log an error message."""
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno

        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.ERROR,
            pathname=filename,
            lineno=lineno,
            msg=message,
            args=(),
            exc_info=None,
        )

        record.processName = multiprocessing.current_process().name

        self.logger.handle(record)

    def critical(self, message):
        """Log a critical message."""
        frame = inspect.currentframe().f_back
        filename = Path(frame.f_code.co_filename).name
        lineno = frame.f_lineno

        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.CRITICAL,
            pathname=filename,
            lineno=lineno,
            msg=message,
            args=(),
            exc_info=None,
        )

        record.processName = multiprocessing.current_process().name

        self.logger.handle(record)

    def set_level(self, level):
        """Set the logging level."""
        self.level = level
        self.logger.setLevel(level)

    def add_file_handler(self, filepath):
        """Add a file handler to the logger."""
        formatter = logging.Formatter(self.format_string)
        file_handler = logging.FileHandler(filepath)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
