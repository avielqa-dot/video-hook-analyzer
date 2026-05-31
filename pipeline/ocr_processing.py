"""
OCR Processing Module
Handles optical character recognition on video frames using EasyOCR.
"""

import os
import logging
from typing import List, Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_easyocr_available() -> bool:
    """
    Check if EasyOCR is available.
    
    Returns:
        bool: True if EasyOCR is installed, False otherwise.
    """
    try:
        import easyocr
        return True
    except ImportError:
        logger.warning("EasyOCR is not installed")
        return False


def perform_ocr_on_frames(frame_paths: List[str], languages: List[str] = ["en"]) -> Optional[Dict]:
    """
    Perform OCR on a list of frame images using EasyOCR.
    
    Args:
        frame_paths (List[str]): List of paths to frame images.
        languages (List[str]): List of language codes to recognize (default: ["en"]).
    
    Returns:
        Dict: Dictionary containing 'text' (aggregated OCR text) and 'frame_results' (per-frame results).
              Returns None if OCR fails.
    """
    try:
        import easyocr
        
        if not frame_paths:
            logger.warning("No frame paths provided for OCR")
            return {
                "text": "",
                "frame_results": []
            }
        
        # Verify all frame files exist
        for frame_path in frame_paths:
            if not os.path.exists(frame_path):
                logger.warning(f"Frame file not found: {frame_path}")
        
        # Initialize the OCR reader
        logger.info(f"Initializing EasyOCR reader for languages: {languages}")
        reader = easyocr.Reader(languages, gpu=False)
        
        # Perform OCR on each frame
        all_text = []
        frame_results = []
        
        for idx, frame_path in enumerate(frame_paths):
            if not os.path.exists(frame_path):
                logger.warning(f"Skipping missing frame: {frame_path}")
                continue
            
            logger.info(f"Processing frame {idx + 1}/{len(frame_paths)}: {frame_path}")
            
            try:
                # Perform OCR on the frame
                results = reader.readtext(frame_path)
                
                # Extract text from results
                frame_text = " ".join([text[1] for text in results if len(text) > 1])
                
                if frame_text.strip():
                    all_text.append(frame_text)
                    frame_results.append({
                        "frame": frame_path,
                        "text": frame_text,
                        "confidence": sum([text[2] for text in results]) / len(results) if results else 0
                    })
                    logger.info(f"Frame {idx + 1} OCR result: {frame_text[:50]}...")
            
            except Exception as e:
                logger.warning(f"Error processing frame {frame_path}: {str(e)}")
                continue
        
        # Combine all text
        combined_text = " ".join(all_text)
        
        result = {
            "text": combined_text,
            "frame_results": frame_results
        }
        
        logger.info(f"OCR complete. Total frames processed: {len(frame_results)}")
        logger.info(f"Combined OCR text: {combined_text[:100]}...")
        
        return result
    
    except ImportError:
        logger.error("EasyOCR is not installed. Install it with: pip install easyocr")
        return None
    except Exception as e:
        logger.error(f"Error during OCR processing: {str(e)}")
        return None


def get_ocr_text(ocr_result: Optional[Dict]) -> str:
    """
    Extract the combined OCR text from the result dictionary.
    
    Args:
        ocr_result (Dict): Result dictionary from perform_ocr_on_frames().
    
    Returns:
        str: The combined OCR text, or an empty string if result is None.
    """
    if ocr_result is None:
        return ""
    return ocr_result.get("text", "")


def get_frame_ocr_results(ocr_result: Optional[Dict]) -> List[Dict]:
    """
    Extract per-frame OCR results from the result dictionary.
    
    Args:
        ocr_result (Dict): Result dictionary from perform_ocr_on_frames().
    
    Returns:
        List[Dict]: List of per-frame OCR results, or an empty list if result is None.
    """
    if ocr_result is None:
        return []
    return ocr_result.get("frame_results", [])
