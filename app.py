from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/threats')
def get_threats():
    return jsonify({
        "threat_count": random.randint(10, 100),
        "threat_types": {
            "DDoS": random.randint(5, 20),
            "Phishing": random.randint(5, 20),
            "Malware": random.randint(5, 20)
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

