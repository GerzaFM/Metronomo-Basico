"""
Utility functions and helpers for the Metronome application.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: int = logging.INFO,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Configure application logging.
    
    Args:
        log_level: Logging level (e.g., logging.INFO, logging.DEBUG)
        log_file: Optional path to log file
        
    Returns:
        Configured root logger
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root
    """
    # Assuming utils.py is in src/utils/
    return Path(__file__).parent.parent.parent


def get_assets_dir() -> Path:
    """
    Get the assets directory.
    
    Returns:
        Path to assets directory
    """
    return get_project_root() / "assets"


def get_sounds_dir() -> Path:
    """
    Get the sounds directory.
    
    Returns:
        Path to sounds directory
    """
    return get_assets_dir() / "sounds"


def get_config_dir() -> Path:
    """
    Get the configuration directory.
    
    Returns:
        Path to config directory
    """
    return get_project_root() / "config"
