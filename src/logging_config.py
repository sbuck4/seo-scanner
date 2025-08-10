import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_level="INFO", log_file=None):
    """
    Setup logging configuration for the SEO Scanner application
    """
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Default log file path
    if log_file is None:
        log_file = log_dir / f"seo-scanner-{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Get log level from environment or parameter
    level = getattr(logging, os.getenv("LOG_LEVEL", log_level).upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Configure specific loggers
    
    # Reduce noise from external libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("streamlit").setLevel(logging.WARNING)
    
    # Create application logger
    logger = logging.getLogger("seo_scanner")
    logger.info(f"Logging initialized - Level: {log_level}, File: {log_file}")
    
    return logger

def get_logger(name):
    """Get a logger instance for a specific module"""
    return logging.getLogger(f"seo_scanner.{name}")