"""
Video Processing Module
Handles video file operations including audio extraction and frame extraction using FFmpeg.
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Tuple, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed and accessible.
    
    Returns:
        bool: True if FFmpeg is installed, False otherwise.
    """
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True,
            timeout=5
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def extract_audio(video_path: str, output_audio_path: str, duration: int = 15) -> bool:
    """
    Extract audio from a video file using FFmpeg.
    
    Args:
        video_path (str): Path to the input video file.
        output_audio_path (str): Path to save the extracted audio file.
        duration (int): Duration in seconds to extract (default: 15).
    
    Returns:
        bool: True if extraction was successful, False otherwise.
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return False
        
        # Extract audio from the first 'duration' seconds
        command = [
            "ffmpeg",
            "-i", video_path,
            "-t", str(duration),
            "-q:a", "9",
            "-n",  # Do not overwrite output file
            output_audio_path
        ]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            return False
        
        if os.path.exists(output_audio_path):
            logger.info(f"Audio extracted successfully: {output_audio_path}")
            return True
        else:
            logger.error("Audio extraction completed but output file not found")
            return False
    
    except subprocess.TimeoutExpired:
        logger.error("Audio extraction timed out")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during audio extraction: {str(e)}")
        return False


def extract_frames(video_path: str, output_dir: str, duration: int = 15, fps: int = 1) -> List[str]:
    """
    Extract frames from a video file using FFmpeg.
    
    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save extracted frames.
        duration (int): Duration in seconds to extract frames from (default: 15).
        fps (int): Frames per second to extract (default: 1).
    
    Returns:
        List[str]: List of paths to extracted frame files, or empty list if extraction failed.
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract frames from the first 'duration' seconds
        output_pattern = os.path.join(output_dir, "frame_%04d.png")
        command = [
            "ffmpeg",
            "-i", video_path,
            "-t", str(duration),
            "-vf", f"fps={fps}",
            "-n",  # Do not overwrite output files
            output_pattern
        ]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            return []
        
        # Collect extracted frame files
        frame_files = sorted([
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith(".png")
        ])
        
        if frame_files:
            logger.info(f"Extracted {len(frame_files)} frames successfully")
            return frame_files
        else:
            logger.warning("No frames were extracted")
            return []
    
    except subprocess.TimeoutExpired:
        logger.error("Frame extraction timed out")
        return []
    except Exception as e:
        logger.error(f"Unexpected error during frame extraction: {str(e)}")
        return []


def get_video_duration(video_path: str) -> float:
    """
    Get the duration of a video file in seconds.
    
    Args:
        video_path (str): Path to the input video file.
    
    Returns:
        float: Duration in seconds, or -1 if unable to determine.
    """
    try:
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return -1
        
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1:noprint_wrappers=1",
            video_path
        ]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout.strip():
            duration = float(result.stdout.strip())
            logger.info(f"Video duration: {duration} seconds")
            return duration
        else:
            logger.warning("Unable to determine video duration using ffprobe")
            return -1
    
    except (ValueError, subprocess.TimeoutExpired):
        logger.error("Error parsing video duration")
        return -1
    except Exception as e:
        logger.error(f"Unexpected error while getting video duration: {str(e)}")
        return -1


def cleanup_temp_files(temp_dir: str) -> bool:
    """
    Clean up temporary files in a directory.
    
    Args:
        temp_dir (str): Path to the temporary directory.
    
    Returns:
        bool: True if cleanup was successful, False otherwise.
    """
    try:
        if not os.path.exists(temp_dir):
            logger.warning(f"Temporary directory not found: {temp_dir}")
            return False
        
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"Deleted: {file_path}")
        
        logger.info("Temporary files cleaned up successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        return False
