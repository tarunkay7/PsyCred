import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


# Define route to save user data
@app.route('/save_user', methods=['POST'])
def save_user():
    # Parse JSON data from request
    user_data = request.json

    # Check if all required fields are present
    if not all(key in user_data for key in ['name', 'age', 'email']):
        return jsonify({'error': 'Incomplete user data'}), 400

    # Connect to the SQLite database
    conn = sqlite3.connect('psy.db')
    cursor = conn.cursor()

    try:
        # Insert user data into the database
        cursor.execute("INSERT INTO Users (name, age, email) VALUES (?, ?, ?)",
                       (user_data['name'], user_data['age'], user_data['email']))
        conn.commit()

        return jsonify({'message': 'User saved successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
