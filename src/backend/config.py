import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


# Function to establish database connection
def connect_db():
    conn = sqlite3.connect('psy.db')
    return conn, conn.cursor()


# Create user API endpoint
@app.route('/create_user', methods=['POST'])
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

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()


# Retrieve user details by ID API endpoint
@app.route('/get_user/<int:user_id>', methods=['GET'])
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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
