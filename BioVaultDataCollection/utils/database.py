import sqlite3

def setup_database():
    conn = sqlite3.connect('data/biometric_data.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute("CREATE TABLE IF NOT EXISTS wpm (value REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS keys_per_sec (value REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS avg_dwell_time (value REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS avg_time_between_keystrokes (value REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS avg_click_dwell_time (value REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS mouse_speed (value REAL)")
    print("Database was created successfully!")
    conn.commit()
    conn.close()

def insert_metric(cursor, table, value):
    if value > 0:  # Only insert if there is activity
        try:
            cursor.execute(f"INSERT INTO {table} (value) VALUES (?)", (value,))
        except sqlite3.OperationalError as e:
            print(f"Failed to insert into {table}: {e}")
