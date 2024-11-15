import mysql.connector
import time
from metrics.keystroke_metrics import KeystrokeMetrics
from metrics.mouse_metrics import MouseMetrics
from utils.database import insert_metric
from pynput import keyboard, mouse
import os
from kc import get_userid
from security import prompt_for_credentials
print(mysql.connector.__version__)
config = {
    'user': 'root',         
    'password': 'secretsquirrels',     
    'host': 'localhost',             
    'database': 'biometric_auth',
    'port': '3307'     
}

def collect_metrics(keystroke_metrics, mouse_metrics, cursor):
    username,password = prompt_for_credentials()
    user_id = get_userid(username,password)
    # Collects key presses
    def on_key_press(key):
        keystroke_metrics.on_press(key)

    # Collects mouse clicks
    def on_mouse_click(x, y, button, pressed):
        mouse_metrics.on_click(x, y, button, pressed)

    # Collects mouse movements
    def on_mouse_move(x, y):
        mouse_metrics.on_move(x, y)

    # Start keyboard listener
    listener_k = keyboard.Listener(on_press=on_key_press)
    listener_m = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move)

    listener_k.start()
    listener_m.start()

    print("Collecting metrics...")
    
    try:
        while True:
            time.sleep(10)

            # Insert metrics if something happened
            if keystroke_metrics.activity_flag or mouse_metrics.activity_flag:
                keystroke_data = keystroke_metrics.calculate_metrics()
                mouse_data = mouse_metrics.calculate_metrics()
              
                # Insert metrics into the database
                insert_metric(cursor, 'wpm', keystroke_data['wpm'],user_id)
                insert_metric(cursor, 'keys_per_sec', keystroke_data['keys_per_sec'],user_id)
                insert_metric(cursor, 'avg_dwell_time', keystroke_data['avg_dwell_time'],user_id)
                insert_metric(cursor, 'avg_time_between_keystrokes', keystroke_data['avg_time_between_keystrokes'],user_id)
                insert_metric(cursor, 'avg_click_dwell_time', mouse_data['avg_click_dwell_time'],user_id)
                insert_metric(cursor, 'mouse_speed', mouse_data['mouse_speed'],user_id)
                print("Inserting metrics...")
                conn.commit()

    except KeyboardInterrupt:
        print("Stopping metric collection...")
    finally:
        listener_k.stop()
        listener_m.stop()

if __name__ == "__main__":

    # Create a connection to MySQL
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Database connection established successfully.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        exit(1)

    keystroke_metrics = KeystrokeMetrics()
    mouse_metrics = MouseMetrics()
    collect_metrics(keystroke_metrics, mouse_metrics, cursor)

    # Close the connection at the end of the program
    conn.close()
