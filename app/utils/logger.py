import logging
import json
from pythonjsonlogger import jsonlogger
from app.config import settings

def setup_logging():
    """Setup JSON logging"""
    logger = logging.getLogger()
    
    # Remove default handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler with JSON formatting
    console_handler = logging.StreamHandler()
    json_formatter = jsonlogger.JsonFormatter()
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)
    
    # Set level
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(log_level)
    
    return logger

logger = setup_logging()