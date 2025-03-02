from flask import Flask, render_template, request, make_response, jsonify
import hashlib
import json
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Encryption function for cookies (basic hashing for demonstration)
def encrypt_cookie(value):
    return hashlib.sha256(value.encode()).hexdigest()

# Store cookies securely (in-memory for simplicity)
cookie_store = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    data = request.json
    name = data.get('name')
    value = data.get('value')
    expiry_days = int(data.get('expiry', 7))  # Convert expiry to integer
    secure_value = encrypt_cookie(value)
    expiration_date = datetime.utcnow() + timedelta(days=expiry_days)

    cookie_store[name] = {
        'value': secure_value,
        'expires': expiration_date.strftime('%Y-%m-%d %H:%M:%S')
    }

    response = make_response(jsonify({"message": "Cookie set successfully"}))
    response.set_cookie(name, secure_value, httponly=True, secure=True, expires=expiration_date)
    return response

@app.route('/get_cookies', methods=['GET'])
def get_cookies():
    return jsonify(cookie_store)

@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    data = request.json
    name = data.get('name')
    
    if name in cookie_store:
        del cookie_store[name]
        response = make_response(jsonify({"message": "Cookie deleted successfully"}))
        response.set_cookie(name, '', expires=0)
        return response
    else:
        return jsonify({"error": "Cookie not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
