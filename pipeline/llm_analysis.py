"""
LLM Analysis Module
Handles hook structure analysis and alternative hook generation using Ollama.
"""

import logging
import json
from typing import Optional, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_ollama_available() -> bool:
    """
    Check if Ollama is available and running.
    
    Returns:
        bool: True if Ollama is available, False otherwise.
    """
    try:
        import ollama
        # Try to list available models to verify Ollama is running
        models = ollama.list()
        return True
    except Exception as e:
        logger.warning(f"Ollama is not available: {str(e)}")
        return False


def analyze_hook_structure(
    transcript: str,
    ocr_text: str,
    model: str = "llama3.1"
) -> Optional[Dict]:
    """
    Analyze the hook structure of a video using Ollama.
    
    Args:
        transcript (str): The transcribed audio text.
        ocr_text (str): The OCR text extracted from frames.
        model (str): The Ollama model to use (default: llama3.1).
    
    Returns:
        Dict: Dictionary containing 'analysis' (structural analysis) and 'hooks' (generated alternatives).
              Returns None if analysis fails.
    """
    try:
        import ollama
        
        if not transcript and not ocr_text:
            logger.warning("No transcript or OCR text provided for analysis")
            return None
        
        # Combine transcript and OCR text
        combined_text = f"Transcript: {transcript}\n\nOn-screen text: {ocr_text}"
        
        # Create the analysis prompt
        analysis_prompt = f"""Analyze the following video hook for its structural elements and effectiveness.

{combined_text}

Please provide:
1. A brief structural analysis of the hook (what makes it work or not work)
2. The primary hook type (e.g., Curiosity, Negative, Question, Controversy, Benefit)
3. Key elements that grab attention
4. Areas for improvement

Format your response as JSON with keys: "structure", "hook_type", "key_elements", "improvements"."""
        
        logger.info(f"Analyzing hook structure using model: {model}")
        
        # Call Ollama for analysis
        response = ollama.generate(
            model=model,
            prompt=analysis_prompt,
            stream=False
        )
        
        analysis_text = response.get("response", "")
        
        # Try to parse JSON from the response
        try:
            # Extract JSON from the response (it might be wrapped in markdown code blocks)
            json_start = analysis_text.find("{")
            json_end = analysis_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = analysis_text[json_start:json_end]
                analysis = json.loads(json_str)
            else:
                analysis = {"raw_analysis": analysis_text}
        except json.JSONDecodeError:
            analysis = {"raw_analysis": analysis_text}
        
        logger.info("Hook structure analysis complete")
        
        return {
            "analysis": analysis,
            "model": model
        }
    
    except ImportError:
        logger.error("Ollama Python library is not installed. Install it with: pip install ollama")
        return None
    except Exception as e:
        logger.error(f"Error during hook analysis: {str(e)}")
        return None


def generate_alternative_hooks(
    transcript: str,
    ocr_text: str,
    num_hooks: int = 3,
    model: str = "llama3.1"
) -> Optional[Dict]:
    """
    Generate alternative hook variations using Ollama.
    
    Args:
        transcript (str): The transcribed audio text.
        ocr_text (str): The OCR text extracted from frames.
        num_hooks (int): Number of alternative hooks to generate (default: 3).
        model (str): The Ollama model to use (default: llama3.1).
    
    Returns:
        Dict: Dictionary containing 'hooks' (list of generated hooks) and 'model' (model used).
              Returns None if generation fails.
    """
    try:
        import ollama
        
        if not transcript and not ocr_text:
            logger.warning("No transcript or OCR text provided for hook generation")
            return None
        
        # Combine transcript and OCR text
        combined_text = f"Transcript: {transcript}\n\nOn-screen text: {ocr_text}"
        
        # Create the generation prompt
        generation_prompt = f"""Based on the following video content, generate {num_hooks} alternative hook variations that could improve viewer engagement.

{combined_text}

Generate {num_hooks} hooks with different approaches:
1. Curiosity Hook: Creates intrigue and makes viewers want to know more
2. Negative Hook: Highlights a problem or pain point
3. Question Hook: Poses a thought-provoking question

Format your response as a JSON array with objects containing "type" and "hook" fields.
Example format: [{{"type": "Curiosity", "hook": "You won't believe what happens next..."}}, ...]"""
        
        logger.info(f"Generating {num_hooks} alternative hooks using model: {model}")
        
        # Call Ollama for hook generation
        response = ollama.generate(
            model=model,
            prompt=generation_prompt,
            stream=False
        )
        
        generation_text = response.get("response", "")
        
        # Try to parse JSON from the response
        hooks = []
        try:
            # Extract JSON array from the response
            json_start = generation_text.find("[")
            json_end = generation_text.rfind("]") + 1
            if json_start != -1 and json_end > json_start:
                json_str = generation_text[json_start:json_end]
                hooks = json.loads(json_str)
            else:
                # If no JSON array found, return raw text
                hooks = [{"type": "Generated", "hook": generation_text}]
        except json.JSONDecodeError:
            hooks = [{"type": "Generated", "hook": generation_text}]
        
        logger.info(f"Generated {len(hooks)} alternative hooks")
        
        return {
            "hooks": hooks,
            "model": model
        }
    
    except ImportError:
        logger.error("Ollama Python library is not installed. Install it with: pip install ollama")
        return None
    except Exception as e:
        logger.error(f"Error during hook generation: {str(e)}")
        return None


def get_analysis_text(analysis_result: Optional[Dict]) -> Dict:
    """
    Extract the analysis from the result dictionary.
    
    Args:
        analysis_result (Dict): Result dictionary from analyze_hook_structure().
    
    Returns:
        Dict: The analysis dictionary, or an empty dict if result is None.
    """
    if analysis_result is None:
        return {}
    return analysis_result.get("analysis", {})


def get_generated_hooks(hooks_result: Optional[Dict]) -> List[Dict]:
    """
    Extract the generated hooks from the result dictionary.
    
    Args:
        hooks_result (Dict): Result dictionary from generate_alternative_hooks().
    
    Returns:
        List[Dict]: List of generated hooks, or an empty list if result is None.
    """
    if hooks_result is None:
        return []
    return hooks_result.get("hooks", [])
