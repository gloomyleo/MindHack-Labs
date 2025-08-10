# redteam_agent.py
from flask import Flask, request, jsonify
import os, openai
app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY', 'YOUR_OPENAI_KEY')
TEMPLATE = "You are an adversarial planner using MITRE ATT&CK. Target: {system}. Techniques: {techniques}. Return numbered steps with ATT&CK IDs."
@app.route('/simulate', methods=['POST'])
def simulate():
    b = request.get_json(force=True); ttps = b.get('techniques', []); sys = b.get('system', 'Windows Server 2019')
    prompt = TEMPLATE.format(system=sys, techniques=', '.join(ttps))
    r = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user','content':prompt}])
    return jsonify({'attack_plan': r.choices[0].message['content']})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
