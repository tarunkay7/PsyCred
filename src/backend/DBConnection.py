from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'psycreditdb.db'

def get_db_connection():
    return sqlite3.connect(DATABASE)

@app.route('/')
def test_connection():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'connected'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
