import logging
import os
from datetime import datetime

def setup_logging(log_level="INFO", log_file=None):
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )

def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)