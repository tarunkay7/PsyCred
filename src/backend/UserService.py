import sqlite3
from flask import Flask, request, jsonify
import random
app = Flask(__name__)


# Function to establish database connection
def connect_db():
    conn = sqlite3.connect('psy.db')
    return conn, conn.cursor()


# Create user API endpoint
@app.route('/api/users/v1/create_user', methods=['POST'])
def create_user():
    conn, cursor = connect_db()

    # Parse JSON data from request
    user_data = request.json

    # Check if all required fields are present
    required_fields = ['name', 'age', 'phone_number', 'education', 'pincode']
    if not all(field in user_data for field in required_fields):
        return jsonify({'error': 'Incomplete user data'}), 400

    try:
        # Insert user data into the database
        cursor.execute('''
            INSERT INTO Users (name, age, phone_number, education, pincode)
            VALUES (?, ?, ?, ?, ?)
        ''', (
        user_data['name'], user_data['age'], user_data['phone_number'], user_data['education'], user_data['pincode']))

        # Retrieve the last inserted primary key value
        user_id = cursor.lastrowid

        # Insert corresponding entry in the SCORES table with default values
        cursor.execute('''
                    INSERT INTO SCORES (user_id, demographic_score, psychometric_test_score)
                    VALUES (?, 0, 0)
                ''', (user_id,))

        cursor.execute('''
                            INSERT INTO creditworthiness_score (user_id, creditworthiness_score)
                            VALUES (?, 0)
                        ''', (user_id,))

        conn.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()


# Retrieve user details by ID API endpoint
@app.route('/api/users/v1/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn, cursor = connect_db()

    try:
        # Fetch user details from the database
        cursor.execute("SELECT * FROM Users WHERE Unique_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            user_details = {
                'Unique_id': user[0],
                'name': user[1],
                'age': user[2],
                'phone_number': user[3],
                'education': user[4],
                'pincode': user[5]
            }
            return jsonify(user_details)
        else:
            return jsonify({'error': 'User not found'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()


# Update user details API endpoint
@app.route('/api/users/v1/update_user/<int:user_id>', methods=['PUT'])
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
# Delete user API endpoint
@app.route('/api/v1/users/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn, cursor = connect_db()

    try:
        # Check if the user exists
        cursor.execute("SELECT * FROM Users WHERE Unique_id = ?", (user_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'User not found'}), 404

        # Delete user from the database
        cursor.execute("DELETE FROM Users WHERE Unique_id = ?", (user_id,))

        # Also delete related entries in other tables
        cursor.execute("DELETE FROM SCORES WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM creditworthiness_score WHERE user_id = ?", (user_id,))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'User deleted successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()


@app.route('/api/users/v1/verify_password', methods=['POST'])
def verify_password():
    conn, cursor = connect_db()

    # Parse JSON data from request
    request_data = request.json

    # Check if phone number is provided
    if 'phone_number' not in request_data:
        return jsonify({'error': 'Phone number is required'}), 400

    # Extract phone number from request data
    phone_number = request_data['phone_number']

    try:
        # Check if the user exists in the database
        cursor.execute("SELECT * FROM Users WHERE phone_number = ?", (phone_number,))
        user = cursor.fetchone()

        if user:
            # Generate OTP (for demonstration, using random 6-digit OTP)
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # For demonstration, printing the OTP
            print("Generated OTP for {}: {}".format(phone_number, otp))

            # Return success response with generated OTP
            return jsonify({'message': 'OTP generated successfully', 'otp': otp}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
