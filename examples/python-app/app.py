from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Python Flask Docker Container!',
        'timestamp': datetime.now().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'production')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
