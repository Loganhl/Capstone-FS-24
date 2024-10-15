from mysql import connector
db_config = {
    'user': 'mashedsnake',
    'password': 'ilovelamp',
    'host': 'mysql',
    'database': 'biometric_auth',
}
def get_users(userid):
    try:
        connection = connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USER_ENTITY WHERE ID = %s;",(userid,))
        db = cursor.fetchall()
        return db
    except Exception:
        print("shhot")


get_users("6242771f-785a-4c47-9c6a-6d5d8c8fffc6")