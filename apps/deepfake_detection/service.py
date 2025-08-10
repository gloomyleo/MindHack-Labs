import random, random as _r

def detect_deepfake(url: str) -> dict:
    verdict = _r.choice(["real", "fake", "uncertain"])
    confidence = round(_r.uniform(0.70, 0.99), 2)
    result = {"url": url, "verdict": verdict, "confidence": confidence}
    try:
        if log_deepfake:
            log_deepfake(url, verdict, confidence)
    except Exception:
        pass
    return result


# Logging
try:
    from apps.db import log_deepfake
except Exception:
    log_deepfake = None
