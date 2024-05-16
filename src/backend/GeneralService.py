import requests
from flask import Flask, request, jsonify
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



@app.route('/gen_questions', methods=['GET'])
def gen_questions():
    """
    Sample API CALL

    resp = requests.get('http://127.0.0.1:5001/gen_questions', json={'Q1': "A",'A1': "A",'Q2': "A",'A2': "A",'Q3': "A",'A3': "A",'Q4': "A",'A4': "A",'Q5': "A",'A5': "A",
    'Q6': "A", 'A6': "A",'Q7': "A",'A7': "A"'Q8': "A",'A8': "A"'Q9': "A",'A9': "A"'Q10': "A",'A10': "A",})
    data = json.loads(resp.json())
    print(data)
    """

    json = request.get_json()
    url = 'https://api.hyperleap.ai/prompts'
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': 'OWQ0MmI1YTdjOTQxNDUyNGFmODBmMDBhZmM5ZGMwYzU='
    }

    data = {
        "promptId": "31764ccc-cff7-4590-8898-e87b2aa905dd",
        "promptVersionId": "d70a9468-f798-4d00-af57-c6523250501e",
        "replacements": {
            "Q1": json['Q1'],
            "A1": json['A1'],
            "Q2": json['Q2'],
            "A2": json['A2'],
            "Q3": json['Q3'],
            "A3": json['A3'],
            "Q4": json['Q4'],
            "A4": json['A4'],
            "Q5": json['Q5'],
            "A5": json['A5'],
            "Q6": json['Q6'],
            "A6": json['A6'],
            "Q7": json['Q7'],
            "A7": json['A7'],
            "Q8": json['Q8'],
            "A8": json['A8'],
            "Q9": json['Q9'],
            "A9": json['A9'],
            "Q10":json['Q10'],
            "A10":json['A10']
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.ok:
        return jsonify(response.json()["choices"][0]["message"]["content"]), 200
    else:
        return jsonify({'error': 'Failed to send prompt'}), response.status_code


@app.route('/rate_answers', methods=['GET'])
def rate_answers():
    """ 
    Sample API CALL

    resp = requests.get('http://127.0.0.1:5001/rate_answers', json={'Q1': "How rich are you?",'A1': "Very.",'Q2': "You responsible bro?",'A2': "Nah."})
    data = json.loads(resp.json())
    print(data["R1"], data["R2"])
    """

    json = request.get_json()
    url = 'https://api.hyperleap.ai/prompts'
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': 'OWQ0MmI1YTdjOTQxNDUyNGFmODBmMDBhZmM5ZGMwYzU='
    }

    data = {
        "promptId": "3206afe9-80a5-4450-ac7f-b4b588e1bb1b",
        "promptVersionId": "fc84a7a4-0131-44f8-91a6-75f5e3b7fc39",
        "replacements": {
            "Q1": json['Q1'],
            "A1": json['A1'],
            "Q2": json['Q2'],
            "A2": json['A2']
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.ok:
        return jsonify(response.json()["choices"][0]["message"]["content"]), 200
    else:
        return jsonify({'error': 'Failed to send prompt'}), response.status_code

@app.route('/rate_mcqs', methods=['GET'])
def rate_mcqs():
    pass


# Update user details API endpoint
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    conn, cursor = connect_db()

    # Parse JSON data from request
    user_data = request.json

    try:
        # Check if the user exists
        cursor.execute("SELECT * FROM Users WHERE Unique_id = ?", (user_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'User not found'}), 404

        # Update user data in the database
        cursor.execute('''
            UPDATE Users
            SET name = ?, age = ?, phone_number = ?, education = ?, pincode = ?
            WHERE Unique_id = ?
        ''', (
        user_data['name'], user_data['age'], user_data['phone_number'], user_data['education'], user_data['pincode'],
        user_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'User updated successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()


# Delete user API endpoint
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn, cursor = connect_db()

    try:
        # Check if the user exists
        cursor.execute("SELECT * FROM Users WHERE Unique_id = ?", (user_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'User not found'}), 404

        # Delete user from the database
        cursor.execute("DELETE FROM Users WHERE Unique_id = ?", (user_id,))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

