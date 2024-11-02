import mysql.connector
import os

def setup_database():
    # Define MySQL connection parameters
    config = {
        'user': 'mashedsnake',         
        'password': 'ilovelamp',     
        'host': 'mysql',             
        'database': 'biometric_auth'     
    }
    
    # Create a connection to MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("CREATE TABLE IF NOT EXISTS wpm (value FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS keys_per_sec (value FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS avg_dwell_time (value FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS avg_time_between_keystrokes (value FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS avg_click_dwell_time (value FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS mouse_speed (value FLOAT)")
    
    print("Database was created successfully!")
    conn.commit()
    cursor.close()
    conn.close()

def insert_metric(cursor, table, value):
    if value > 0:  # Only insert if there is activity
        try:
            cursor.execute(f"INSERT INTO {table} (value) VALUES (%s)", (value,))
        except mysql.connector.Error as e:
            print(f"Failed to insert into {table}: {e}")
