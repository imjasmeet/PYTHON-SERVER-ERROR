"""
Logging configuration for the Flask application.
This module provides different logging configurations for development and production.
"""

import os
import logging
import sys
from datetime import datetime

def get_log_level():
    """Get log level from environment variable."""
    level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    return level_map.get(level, logging.INFO)

def setup_logging(log_level=None):
    """
    Setup logging with different levels and formatting.
    
    Args:
        log_level: Optional log level override
        
    Returns:
        Logger instance
    """
    if log_level is None:
        log_level = get_log_level()
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Clear any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure root logger
    root_logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(log_format, date_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # File handler for errors only
    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # File handler for debug logs (if debug level is enabled)
    if log_level <= logging.DEBUG:
        debug_handler = logging.FileHandler('logs/debug.log')
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        root_logger.addHandler(debug_handler)
    
    # Set Flask logger level
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    
    return logging.getLogger(__name__)

def get_logger(name=None):
    """Get a logger instance."""
    if name is None:
        name = __name__
    return logging.getLogger(name)

# Log level descriptions
LOG_LEVELS = {
    'DEBUG': 'Detailed information for debugging',
    'INFO': 'General information about program execution',
    'WARNING': 'Warning messages for potentially problematic situations',
    'ERROR': 'Error messages for serious problems',
    'CRITICAL': 'Critical error messages for fatal problems'
}

def print_log_levels():
    """Print available log levels and their descriptions."""
    print("Available Log Levels:")
    for level, description in LOG_LEVELS.items():
        print(f"  {level}: {description}")
    print(f"\nCurrent log level: {os.environ.get('LOG_LEVEL', 'INFO')}")

if __name__ == '__main__':
    print_log_levels() 