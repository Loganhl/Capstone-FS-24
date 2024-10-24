from pynput import keyboard
import time
from collections import defaultdict

keystrokes = []
keystroke_times = [] 
key_pair_times = defaultdict(lambda: defaultdict(list))
error_count = 0  

def on_press(key):
    global error_count
    current_time = time.time()
    
    try:
        char = key.char  
        if char:  
            keystrokes.append(char)  
            keystroke_times.append(current_time)  
            
            if len(keystrokes) > 1:
                previous_char = keystrokes[-2] 
                time_between = current_time - keystroke_times[-2]  
                key_pair_times[previous_char][char].append(time_between)  
    except AttributeError:
        if key == keyboard.Key.backspace or key == keyboard.Key.delete:
            error_count += 1 

def calculate_metrics(start_time):
    global keystrokes, keystroke_times, error_count

    elapsed_time = time.time() - start_time

    keys_count = len(keystrokes)
    wpm = (keys_count / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0  
    keys_per_second = keys_count / elapsed_time if elapsed_time > 0 else 0

    avg_time_between_keystrokes = (
        sum(keystroke_times[i] - keystroke_times[i - 1] for i in range(1, len(keystroke_times)))
        / (len(keystroke_times) - 1) if len(keystroke_times) > 1 else 0
    )

    keystrokes = []
    keystroke_times = []
    error_count_snapshot = error_count
    error_count = 0

    return wpm, keys_count, keys_per_second, avg_time_between_keystrokes, error_count_snapshot

def print_key_pair_times():
    print("Time between key pairs:")
    for key1, pairs in key_pair_times.items():
        for key2, times in pairs.items():
            avg_time = sum(times) / len(times) if times else 0  
            print(f"Time between '{key1}' and '{key2}': {avg_time:.12f} seconds")

    key_pair_times.clear()
