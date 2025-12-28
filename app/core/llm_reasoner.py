import requests
import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

def reason(payload: dict) -> str:
    """
    Cognitive arbitration using Ollama.
    Synthesizes technical data into a structured reasoning string.
    """
    prompt = f"""
You are a professional Indian market equity analyst.
Analyze the following quantitative data and provide a detailed structured response.

REQUIRED OUTPUT FORMAT:
• VERDICT: [BUY / SELL / HOLD]
• CONFIDENCE: [0.0 - 1.0]
• RISK FACTORS: [Key risks identified]
• REASONING: [Step-by-step logic]

DATA:
{json.dumps(payload, indent=2)}
"""
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=30)
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        logger.error(f"Ollama reasoning failed: {e}")
        return f"AI Reasoning Unavailable. Error: {str(e)}. Please ensure Ollama is running with {MODEL}."
