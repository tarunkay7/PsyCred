import requests
from flask import Flask, request, jsonify
from twilio.rest import Client
import sqlite3
import random

app = Flask(__name__)

# Twilio credentials


# Function to establish database connection
def connect_db():
    conn = sqlite3.connect('psy.db')
    return conn, conn.cursor()

# Generate OTP
# Global variable to store OTP
global_otp = None

# Generate OTP
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# Route to generate OTP
@app.route('/api/users/v1/generate_otp', methods=['GET'])
def generate_otp_route():
    global global_otp
    global_otp = generate_otp()
    return jsonify({'otp': global_otp}), 200

# Route to verify OTP
@app.route('/api/users/v1/verify_otp', methods=['POST'])
def verify_otp():
    global global_otp

    # Parse JSON data from request
    request_data = request.json

    # Check if OTP is provided
    if 'otp' not in request_data:
        return jsonify({'error': 'OTP is required'}), 400

    # Extract OTP from request data
    otp = request_data['otp']

    # Verify if the submitted OTP matches the stored OTP
    if otp == global_otp:
        return jsonify({'message': 'OTP verification successful'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 401


@app.route('/api/hyperleap/v1/persona', methods=['POST'])
def hyperleap_persona():
    # Extract JSON data from the request
    request_data = request.json

    # Check if the required fields are present
    if 'personaId' not in request_data or 'questions' not in request_data:
        return jsonify({'error': 'Persona ID and questions are required'}), 400

    # Construct the API endpoint
    api_url = 'https://api.hyperleap.ai/conversations/persona'

    # Construct the request headers
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': ''  # Replace with your actual API key
    }

    try:
        # Make the API call
        response = requests.post(api_url, headers=headers, json=request_data)
        response_data = response.json()

        return jsonify(response_data), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/send_prompt', methods=['GET'])
def send_prompt():
    # Define the URL and headers
    url = 'https://api.hyperleap.ai/prompts'
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': 'OWQ0MmI1YTdjOTQxNDUyNGFmODBmMDBhZmM5ZGMwYzU='  # Replace with your API key
    }

    # Define the JSON data
    data = {
        "promptId": "31764ccc-cff7-4590-8898-e87b2aa905dd",
        "promptVersionId": "d70a9468-f798-4d00-af57-c6523250501e",
        "replacements": {
            "Q1": "Q1 value",
            "A1": "A1 value",
            "Q2": "Q2 value",
            "A2": "A2 value",
            "Q3": "Q3 value",
            "A3": "A3 value",
            "Q4": "Q4 value",
            "A4": "A4 value",
            "Q5": "Q5 value",
            "A5": "A5 value",
            "Q6": "Q6 value",
            "A6": "A6 value",
            "Q7": "Q7 value",
            "A7": "A7 value",
            "Q8": "Q8 value",
            "A8": "A8 value",
            "Q9": "Q9 value",
            "A9": "A9 value",
            "Q10": "Q10 value",
            "A10": "A10 value"
        }
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.ok:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to send prompt'}), response.status_code



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
