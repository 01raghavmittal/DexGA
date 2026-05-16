"""Logging configuration and utilities."""

import logging
import logging.handlers
from pathlib import Path
from config.settings import LOG_FILE, ERROR_LOG_FILE, LOG_FORMAT, LOG_LEVEL, MAX_LOG_SIZE


class LoggerSetup:
    """Logger setup and configuration."""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get or create a logger instance.
        
        Args:
            name: Logger name (usually __name__)
            
        Returns:
            Configured logger instance
        """
        if name in LoggerSetup._loggers:
            return LoggerSetup._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Main log handler
        main_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=5
        )
        main_handler.setLevel(getattr(logging, LOG_LEVEL))
        main_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(main_handler)
        
        # Error log handler
        error_handler = logging.handlers.RotatingFileHandler(
            ERROR_LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(error_handler)
        
        # Console handler (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)
        
        LoggerSetup._loggers[name] = logger
        return logger


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get logger.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return LoggerSetup.get_logger(name)
