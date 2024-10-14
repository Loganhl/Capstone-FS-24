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
#probably want to add user id variable as parameter in the path

@app.route('/api/keyboardanomaly:userid',methods=('GET','POST'))
def keyboardanomaly():
    #WILL CONTINUE ONCE IVE HAD MY COFFEE!
    
    connection = mysql.connector.connect(**db_config)
    insertquery = ''  
#create an endpoint for mouse anomaly data to be sent to.
@app.route('/api/mouseanomaly:userid',methods=('POST'))
def mouseanomaly():
    return
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
