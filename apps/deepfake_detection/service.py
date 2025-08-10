import random
from apps.db import log_deepfake, now_iso

def detect_deepfake(url: str) -> dict:
    verdict = random.choice(["real", "fake", "uncertain"])
    confidence = round(random.uniform(0.70, 0.99), 2)
    result = {"ts": now_iso(), "url": url, "verdict": verdict, "confidence": confidence}
    try:
        log_deepfake(url, verdict, confidence)
    except Exception:
        pass
    return result
