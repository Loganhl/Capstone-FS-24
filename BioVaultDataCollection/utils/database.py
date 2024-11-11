import mysql.connector
import os
def insert_metric(cursor, table, value,user_id):
    if value > 0:  # Only insert if there is activity
        try:
            cursor.execute(f"INSERT INTO {table} (value) VALUES (%s)", (value,))
        except mysql.connector.Error as e:
            print(f"Failed to insert into {table}: {e}")
