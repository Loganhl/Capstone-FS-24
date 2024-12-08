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

    def insert_metrics(self, table_name, metrics, user_id):
        if self.conn is None:
            print("Database connection not established. Cannot insert data.")
            return
        try:
            # Build query dynamically for multiple columns
            columns = ', '.join(metrics.keys()) + ', USER_ID'
            placeholders = ', '.join(['%s'] * (len(metrics) + 1))  # One extra placeholder for USER_ID
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Prepare the values tuple
            values = list(metrics.values()) + [user_id]

            # Execute and commit
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"Inserted metrics into table {table_name}: {metrics}")
        except mysql.connector.Error as e:
            print(f"Error inserting data into table {table_name}: {e}")


    def insert_regular_metric(self, table_name, value, user_id):
        if self.conn is None:
            print("Database connection not established. Cannot insert data.")
            return
        try:
            # Insert value into a table with a single 'value' column and a 'USER_ID' column
            query = f"INSERT INTO {table_name} (value, USER_ID) VALUES (%s, %s)"
            self.cursor.execute(query, (value, user_id))
            self.conn.commit()
            print(f"Inserted value {value} into table {table_name}.")
        except mysql.connector.Error as e:
            print(f"Error inserting data into table {table_name}: {e}")

    def check_training_data_complete(self, user_id):
        if self.conn is None:
            print("Database connection not established. Cannot check training data.")
            return False
        try:
            # Query to count rows with the specific USER_ID
            query_keystroke = f"SELECT COUNT(*) FROM keystroke_training_data WHERE USER_ID = '{user_id}'"
            query_mouse = f"SELECT COUNT(*) FROM mouse_training_data WHERE USER_ID = '{user_id}'"

            # Execute queries with parameterized input
            self.cursor.execute(query_keystroke)
            keystroke_count = self.cursor.fetchone()[0]

            self.cursor.execute(query_mouse)
            mouse_count = self.cursor.fetchone()[0]

            # Check if counts meet the condition
            return keystroke_count >= 100 and mouse_count >= 100
        except mysql.connector.Error as e:
            print(f"Error checking training data: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
