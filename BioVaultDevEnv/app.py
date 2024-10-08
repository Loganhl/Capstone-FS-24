from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'user': 'mashedsnake',
    'password': 'ilovelamp',
    'host': 'mysql',
    'database': 'biometric_auth',
}

@app.route('/')
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE();")
    db = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify({"message": f"Connected to {db[0]}!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
