# pqc_benchmark.py
from flask import Flask, jsonify
import time, platform, psutil
app = Flask(__name__)
def simulate(base): t0=time.time(); time.sleep(base); return round(time.time()-t0,3)
@app.route('/benchmark', methods=['GET'])
def benchmark():
    return jsonify({
        'device': platform.node(),
        'os': platform.platform(),
        'algorithms': {'Kyber': simulate(0.08), 'Dilithium': simulate(0.12), 'Falcon': simulate(0.15)},
        'cpu_percent': psutil.cpu_percent(interval=1),
        'mem_percent': psutil.virtual_memory().percent
    })
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
