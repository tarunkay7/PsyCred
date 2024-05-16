from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# Configuration
CONNECTION_STRING = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:dbserverpsy.database.windows.net,1433;Database=psycredDB;Uid={your_user_name};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated'


def get_db_connection():
    return pyodbc.connect(CONNECTION_STRING)


@app.route('/')
def index():
    try:
        conn = get_db_connection()
        if conn:
            return jsonify("Connected")
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
