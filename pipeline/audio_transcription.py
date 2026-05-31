"""
Audio Transcription Module
Handles audio transcription using Faster-Whisper for local processing.
"""

import os
import logging
from typing import Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_whisper_available() -> bool:
    """
    Check if Faster-Whisper is available.
    
    Returns:
        bool: True if Faster-Whisper is installed, False otherwise.
    """
    try:
        from faster_whisper import WhisperModel
        return True
    except ImportError:
        logger.warning("Faster-Whisper is not installed")
        return False


def transcribe_audio(audio_path: str, model_size: str = "base") -> Optional[Dict[str, str]]:
    """
    Transcribe audio using Faster-Whisper.
    
    Args:
        audio_path (str): Path to the audio file.
        model_size (str): Size of the Whisper model to use (tiny, base, small, medium, large).
                         Default is 'base' for a balance between speed and accuracy.
    
    Returns:
        Dict[str, str]: Dictionary containing 'text' (transcription) and 'language' (detected language).
                       Returns None if transcription fails.
    """
    try:
        from faster_whisper import WhisperModel
        
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None
        
        # Initialize the Whisper model
        logger.info(f"Loading Whisper model (size: {model_size})...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        
        # Transcribe the audio
        logger.info("Transcribing audio...")
        segments, info = model.transcribe(audio_path, language="en")
        
        # Combine all segments into a single text
        full_text = " ".join([segment.text for segment in segments])
        
        result = {
            "text": full_text,
            "language": info.language,
            "duration": info.duration
        }
        
        logger.info(f"Transcription complete. Detected language: {info.language}")
        logger.info(f"Transcribed text: {full_text[:100]}...")
        
        return result
    
    except ImportError:
        logger.error("Faster-Whisper is not installed. Install it with: pip install faster-whisper")
        return None
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        return None


def get_transcription_text(transcription_result: Optional[Dict]) -> str:
    """
    Extract the transcription text from the result dictionary.
    
    Args:
        transcription_result (Dict): Result dictionary from transcribe_audio().
    
    Returns:
        str: The transcribed text, or an empty string if result is None.
    """
    if transcription_result is None:
        return ""
    return transcription_result.get("text", "")


def get_detected_language(transcription_result: Optional[Dict]) -> str:
    """
    Extract the detected language from the result dictionary.
    
    Args:
        transcription_result (Dict): Result dictionary from transcribe_audio().
    
    Returns:
        str: The detected language code, or an empty string if result is None.
    """
    if transcription_result is None:
        return ""
    return transcription_result.get("language", "")
