from flask import Flask, jsonify,request,Response,make_response
import mysql.connector
from mysql import connector
from helper import get_users

app = Flask(__name__)
# CORS(app,resources={r"/api/*":{"origins":"*"}})
# MySQL connection configuration
db_config = {
    'user': 'mashedsnake',
    'password': 'ilovelamp',
    'host': 'mysql',
    'database': 'biometric_auth',
}
#probably want to add user id variable as parameter in the path

@app.route('/api/anomalies/<userid>',methods=('GET','POST'))

def getuseranomalies(userid):
    user = get_users(userid)
    #just returns the user object for the moments
    return jsonify(user)
@app.route('/api/activeusers',methods=('GET','POST'))
def getactiveusers():
    print(request.args)
    print(request.data)
    connection = connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM USER_ENTITY;')
    db = cursor.fetchall()
    return jsonify(db)
@app.route('/api/keyboardanomaly')
def keyboardanomaly():
    connection =connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM USER_ENTITY;")
    db = cursor.fetchall()
    #WILL CONTINUE ONCE IVE HAD MY COFFEE!
    if request.data == None:
        request.se
        return jsonify({"Error":f"users: {db}"})  
    else:
        
        print(request)
        # return jsonify({"idk":f"users: {db[1]}"})
        return jsonify(db)
#create an endpoint for mouse anomaly data to be sent to.
@app.route('/api/mouseanomaly/<userid>',methods=['POST'])
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
