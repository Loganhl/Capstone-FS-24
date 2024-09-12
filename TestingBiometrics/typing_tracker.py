from pynput import keyboard
import time
from collections import defaultdict
import re
from database import Database

class TypingTracker:
    def __init__(self, db_name="database.db"): #initializes all  attributes below and names database
        self.db = Database(db_name) # Name of database file
        self.start_time = time.time() # start time to calculate elapsed time
        self.last_key_time = self.start_time # time of lat key press to calculate intervals
        self.total_key_presses = 0 # counts total number of key presses
        self.time_intervals = []  # stores all time intervals
        self.key_pair_times = defaultdict(list)  # stores key-pair time intervals
        self.previous_key = None  # keeps track of the last key pressed
        self.text = ""  # To store the text typed by the user

        
        self.db.init_db() # creates tables in the database if they do not exist and initialized database

    def on_press(self, key):
        current_time = time.time() #records current time when any key is pressed

        #calculates the time since the last key was pressed
        time_interval = current_time - self.last_key_time
        self.time_intervals.append(time_interval)
        self.total_key_presses += 1
        self.last_key_time = current_time

        
        current_key = self.get_key_name(key)# retrives current key

        
        if self.previous_key is not None and current_key is not None: #records a key-pair time is there is a previous key
            self.key_pair_times[(self.previous_key, current_key)].append(time_interval)

        
        self.previous_key = current_key #update previous key to current key

        #appends key to text
        if current_key: 
            self.text += current_key

    #triggered when a key is released
    def on_release(self, key):
        if key == keyboard.Key.esc:
            #stops listening when 'esc' is pressed
            return False

    #starts listening to keyboard events
    def start_typing(self):
        print("Typing started. Press 'ESC' to stop.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    
    def calculate_metrics(self):
        total_time = time.time() - self.start_time #total time spent typing
        average_interval = sum(self.time_intervals) / len(self.time_intervals) if self.time_intervals else 0 # average time between key presses

        #calculates wpm
        word_count = len(re.findall(r'\b\w+\b', self.text))  
        wpm = (word_count / total_time) * 60 if total_time > 0 else 0

        # calculates average time for key pairs
        key_pair_averages = {}
        for pair, times in self.key_pair_times.items():
            key_pair_averages[pair] = sum(times) / len(times)

       #sends data to database
        self.db.save_to_db(wpm, average_interval, key_pair_averages)

        print("Averaged typing data has been saved to the database.")


    #converst the key object int a human-readable string
    def get_key_name(self, key):
        try:
            if key.char:
                return key.char
        except AttributeError:
            if key == keyboard.Key.space:
                return ' '
            elif key == keyboard.Key.enter:
                return '\n'
        return None