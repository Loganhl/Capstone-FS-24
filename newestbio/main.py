import time
import csv
from pynput import keyboard, mouse
from keyboard_metrics import calculate_metrics, on_press
from mouse_metrics import calculate_mouse_metrics, calculate_double_click_speed, on_click, on_move

# Change tracking duration as needed
tracking_duration = 10 

# Define CSV file names for each metric
wpm_file = 'wpm.csv'
total_keys_file = 'total_keys.csv'
keys_per_second_file = 'keys_per_second.csv'
avg_time_between_keystrokes_file = 'avg_time_between_keystrokes.csv'
error_count_file = 'error_count.csv'
mouse_speed_file = 'mouse_speed.csv'
click_count_file = 'click_count.csv'
double_click_speed_file = 'double_click_speed.csv'

listener_keyboard = keyboard.Listener(on_press=on_press)
listener_mouse = mouse.Listener(on_click=on_click, on_move=on_move)

listener_keyboard.start()
listener_mouse.start()

print("Starting continuous tracking...")

def write_data_to_csv(file_name, data):
    if data != 0:  # Only write data if it's not zero
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data])  # Wrap data in a list for writing
    else:
        print(f"Skipped writing {data} to {file_name} (value is zero).")

try:
    # Write headers for each metric CSV file
    for file_name in [wpm_file, total_keys_file, keys_per_second_file, avg_time_between_keystrokes_file,
                      error_count_file, mouse_speed_file, click_count_file, double_click_speed_file]:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{file_name.split('.')[0]}"])  # Use the filename as the header

    while True:
        start_time = time.time()
        time.sleep(tracking_duration)

        # Get keyboard metrics
        wpm, keys_count, keys_per_second, avg_time_between_keystrokes, error_count = calculate_metrics(start_time)

        # Get mouse metrics
        avg_mouse_speed, click_count = calculate_mouse_metrics()
        double_click_speed = calculate_double_click_speed()

        # Write each metric to its respective CSV file
        write_data_to_csv(wpm_file, wpm)
        write_data_to_csv(total_keys_file, keys_count)
        write_data_to_csv(keys_per_second_file, keys_per_second)
        write_data_to_csv(avg_time_between_keystrokes_file, avg_time_between_keystrokes)
        write_data_to_csv(error_count_file, error_count)
        write_data_to_csv(mouse_speed_file, avg_mouse_speed)
        write_data_to_csv(click_count_file, click_count)
        write_data_to_csv(double_click_speed_file, double_click_speed)

except KeyboardInterrupt:
    print("Stopping listeners...")
    listener_keyboard.stop()
    listener_mouse.stop()
    print("Tracking stopped.")
