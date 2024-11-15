import mysql.connector

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

    def insert_metric(self, table_name, value, user_id):


        if self.conn is None:
            print("Database connection not established. Cannot insert data.")
            return
        try:
            query = f"INSERT INTO {table_name} (value, USER_ID) VALUES (%s,%s)"
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
