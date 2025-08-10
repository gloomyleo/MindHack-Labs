import os, openai
from apps.db import log_redteam

openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY")

TEMPLATE = """You are an adversarial planner using MITRE ATT&CK.
Target system: {system}
Techniques to simulate: {techniques}

Return a concise, numbered attack plan with ATT&CK IDs referenced."""

def plan_attack(system: str, techniques: list[str]) -> str:
    prompt = TEMPLATE.format(system=system, techniques=', '.join(techniques))
    try:
        r = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        plan = r.choices[0].message["content"]
        try:
            log_redteam(system, techniques, plan)
        except Exception:
            pass
        return plan
    except Exception as e:
        return f"Error: {e}"
