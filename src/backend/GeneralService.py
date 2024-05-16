import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


# Function to establish database connection
def connect_db():
    conn = sqlite3.connect('psy.db')
    return conn, conn.cursor()
@app.route('/api/v1/setlanguage', methods=['POST'])
def set_language():
    # Assuming JSON data is received in the request body
    lang_data = request.json

    print(lang_data)

    return 'Language set successfully', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)