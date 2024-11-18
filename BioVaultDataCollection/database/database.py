import mysql.connector
from kc import get_userid


class Database:
    def __init__(self):

        config = {
            'user': 'root',
            'password': 'secretsquirrels',
            'host': 'localhost',
            'database': 'biometric_auth',
            'port': '3307'
        }

        self.conn = None
        self.cursor = None

        try:
            self.conn = mysql.connector.connect(**config)
            self.cursor = self.conn.cursor()
            print("MySQL Database connection established successfully.")
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            self.conn = None

    def insert_metric(self, table_name, value, user_id, min_threshold=0.01):
        user_id = get_userid('user@user.com', 'user')
        if self.conn is None:
            print("Database connection not established. Cannot insert data.")
            return
        if value <= min_threshold:
            print(f"Value {value} below threshold {min_threshold}. Skipping insertion into {table_name}.")
            return
        try:
            query = f"INSERT INTO {table_name} (value, USER_ID) VALUES (%s, %s)"
            self.cursor.execute(query, (value, user_id))
            self.conn.commit()
            print(f"Inserted value {value} into table {table_name}.")
        except mysql.connector.Error as e:
            print(f"Error inserting data into table {table_name}: {e}")

    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
#git push origin main lol


# the best way to have all the fun in the world is to eat cookies

#the best way to have all th efun in the world is to eat all the cookies possible tj