# deepfake_api.py
from flask import Flask, request, jsonify
import random
app = Flask(__name__)
@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json(force=True); url = data.get('url', 'unknown')
    verdict = random.choice(['real','fake','uncertain']); confidence = round(random.uniform(0.70,0.99),2)
    return jsonify({'url':url,'verdict':verdict,'confidence':confidence})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
