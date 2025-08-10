from flask import Flask, request, jsonify, render_template_string
import os, time, platform, psutil
from apps.prompt_injection.service import run_prompt_test
from apps.deepfake_detection.service import detect_deepfake
from apps.ai_redteam.service import plan_attack
from apps.pqc_benchmark.service import run_benchmarks
from apps.db import init_db, get_conn

app = Flask(__name__)
init_db()

HOME_HTML = '''
<!doctype html>
<html>
<head><title>MindHack-Labs (Python Only)</title>
<style>
body{font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding:30px; color:#111}
.card{border:1px solid #e5e7eb; border-radius:14px; padding:16px; margin:12px 0; box-shadow:0 4px 20px rgba(0,0,0,.05)}
h1{font-size:28px} h2{font-size:20px}
code{background:#f3f4f6; padding:2px 6px; border-radius:6px}
</style>
</head>
<body>
<h1>MindHack-Labs — Python Only</h1>
<div class="card">
  <h2>Prompt Injection Testing</h2>
  <p>POST <code>/api/prompt-test</code> with JSON: <code>{"prompt":"..."} </code></p>
</div>
<div class="card">
  <h2>Deepfake Detection (stub)</h2>
  <p>POST <code>/api/deepfake/detect</code> with JSON: <code>{"url":"http://..."}</code></p>
</div>
<div class="card">
  <h2>AI Red Team Planner</h2>
  <p>POST <code>/api/redteam/simulate</code> with JSON: <code>{"system":"...", "techniques":["T1059"]}</code></p>
</div>
<div class="card">
  <h2>PQC Benchmark</h2>
  <p>GET <code>/api/pqc/benchmark</code></p>
</div>
</body>
</html>'''

@app.get("/")
def home():
    return render_template_string(HOME_HTML)

@app.post("/api/prompt-test")
def api_prompt():
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    result = run_prompt_test(prompt)
    return jsonify(result)

@app.post("/api/deepfake/detect")
def api_deepfake():
    data = request.get_json(force=True)
    url = data.get("url", "")
    result = detect_deepfake(url)
    return jsonify(result)

@app.post("/api/redteam/simulate")
def api_redteam():
    data = request.get_json(force=True)
    system = data.get("system", "Windows Server 2019")
    techniques = data.get("techniques", [])
    result = plan_attack(system, techniques)
    return jsonify({"attack_plan": result})

@app.get("/api/pqc/benchmark")
def api_pqc():
    return jsonify(run_benchmarks())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)

@app.get("/api/logs/<table>")
def api_logs(table):
    allowed = {"prompt_tests","deepfake_results","redteam_plans","pqc_runs"}
    if table not in allowed:
        return {"error":"invalid table"}, 400
    conn = get_conn(); c = conn.cursor()
    rows = [dict(zip([d[0] for d in c.description], r)) for r in c.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 100")]
    conn.close()
    return {"rows": rows}
