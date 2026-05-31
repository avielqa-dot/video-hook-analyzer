"""
Helper Utilities
Common utility functions for the Video Hook Analyzer.
"""

import os
import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (str): Path to the directory.
    
    Returns:
        bool: True if directory exists or was created successfully, False otherwise.
    """
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        return False


def get_file_size(file_path: str) -> Optional[int]:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        int: File size in bytes, or None if file doesn't exist.
    """
    try:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            logger.info(f"File size: {file_path} = {size} bytes")
            return size
        else:
            logger.warning(f"File not found: {file_path}")
            return None
    except Exception as e:
        logger.error(f"Error getting file size: {str(e)}")
        return None


def is_valid_video_file(file_path: str) -> bool:
    """
    Check if a file is a valid video file based on extension.
    
    Args:
        file_path (str): Path to the file.
    
    Returns:
        bool: True if the file has a valid video extension, False otherwise.
    """
    valid_extensions = {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".m4v"}
    file_extension = Path(file_path).suffix.lower()
    is_valid = file_extension in valid_extensions
    
    if is_valid:
        logger.info(f"Valid video file: {file_path}")
    else:
        logger.warning(f"Invalid video file extension: {file_extension}")
    
    return is_valid


def get_temp_directory() -> str:
    """
    Get the path to the temporary directory for the project.
    
    Returns:
        str: Path to the temporary directory.
    """
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "temp")
    ensure_directory_exists(temp_dir)
    return temp_dir


def generate_session_id() -> str:
    """
    Generate a unique session ID for processing.
    
    Returns:
        str: A unique session ID based on timestamp.
    """
    import time
    import hashlib
    
    timestamp = str(time.time())
    session_id = hashlib.md5(timestamp.encode()).hexdigest()[:8]
    logger.info(f"Generated session ID: {session_id}")
    return session_id


def format_duration(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.
    
    Args:
        seconds (float): Duration in seconds.
    
    Returns:
        str: Formatted duration string (e.g., "1m 30s").
    """
    if seconds < 0:
        return "Unknown"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    
    if minutes == 0:
        return f"{secs}s"
    elif minutes < 60:
        return f"{minutes}m {secs}s"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m {secs}s"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text (str): The text to truncate.
        max_length (int): Maximum length of the text (default: 100).
        suffix (str): Suffix to add if text is truncated (default: "...").
    
    Returns:
        str: Truncated text.
    """
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - len(suffix)] + suffix


def safe_remove_file(file_path: str) -> bool:
    """
    Safely remove a file, handling errors gracefully.
    
    Args:
        file_path (str): Path to the file to remove.
    
    Returns:
        bool: True if file was removed or didn't exist, False if removal failed.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File removed: {file_path}")
            return True
        else:
            logger.info(f"File does not exist: {file_path}")
            return True
    except Exception as e:
        logger.error(f"Error removing file {file_path}: {str(e)}")
        return False
