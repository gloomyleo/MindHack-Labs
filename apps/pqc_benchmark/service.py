import time, platform, psutil
from apps.db import log_pqc, now_iso

def simulate(base):
    t0 = time.time(); time.sleep(base); return round((time.time()-t0)*1000, 1)  # ms

def run_benchmarks():
    res = {
        "ts": now_iso(),
        "device": platform.node(),
        "os": platform.platform(),
        "algorithms": {
            "Kyber": simulate(0.08),
            "Dilithium": simulate(0.12),
            "Falcon": simulate(0.15),
        },
        "cpu_percent": psutil.cpu_percent(interval=1),
        "mem_percent": psutil.virtual_memory().percent
    }
    try:
        log_pqc(res["device"], res["os"], res["algorithms"], res["cpu_percent"], res["mem_percent"])
    except Exception:
        pass
    return res
