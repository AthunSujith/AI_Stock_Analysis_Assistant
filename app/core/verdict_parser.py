import re
from typing import Dict, Any

def parse(text: str) -> Dict[str, Any]:
    """
    Parses the LLM output text to extract structured verdict and confidence.
    """
    # Look for BUY/SELL/HOLD, case-insensitive
    verdict_match = re.search(r"\b(BUY|SELL|HOLD)\b", text, re.IGNORECASE)
    # Look for a probability/confidence value (0.0 to 1.0)
    prob_match = re.search(r"(?:confidence|probability)?[:\s]*(0\.\d+|1\.0|1)", text, re.IGNORECASE)

    verdict = verdict_match.group(1).upper() if verdict_match else "HOLD"
    confidence = float(prob_match.group(1)) if prob_match else 0.5

    return {
        "verdict": verdict,
        "confidence": confidence,
        "raw_reasoning": text.strip()
    }
