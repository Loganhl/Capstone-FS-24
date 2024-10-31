import time
from pynput import keyboard

class KeystrokeMetrics:
    def __init__(self, interval_duration=10, idle_threshold=1, avg_word_length=5):
        self.interval_duration = interval_duration
        self.idle_threshold = idle_threshold
        self.avg_word_length = avg_word_length
        self.start_time = time.time()
        self.key_count = 0
        self.char_count = 0
        self.dwell_times = []
        self.key_intervals = []
        self.key_press_times = {}
        self.last_key_time = None
        self.active_typing_time = 0
        self.activity_flag = False

        # Start the keyboard listener
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def on_press(self, key):
        current_time = time.time()

        # Check for idle time and adjust active typing time
        if self.last_key_time and (current_time - self.last_key_time) > self.idle_threshold:
            # Reset the active typing time for idle periods
            self.active_typing_time -= (current_time - self.last_key_time)

        # Record time between keystrokes for metrics
        if self.last_key_time:
            self.key_intervals.append(current_time - self.last_key_time)

        # Update key count and active typing time
        self.key_count += 1
        if hasattr(key, 'char') and key.char is not None:
            self.char_count += 1
        self.active_typing_time += current_time - (self.last_key_time or current_time)
        self.last_key_time = current_time
        self.key_press_times[key] = current_time
        self.activity_flag = True

    def on_release(self, key):
        current_time = time.time()

        # Calculate dwell time for key
        if key in self.key_press_times:
            dwell_time = current_time - self.key_press_times[key]
            self.dwell_times.append(dwell_time)
            del self.key_press_times[key]

    def calculate_metrics(self):
        words_typed = self.char_count / self.avg_word_length
        active_time_minutes = (self.active_typing_time / 60) if self.active_typing_time > 0 else 1
        wpm = (words_typed / active_time_minutes) if active_time_minutes > 0 else 0

        # Adjusting for idle periods when calculating keys per second
        if self.active_typing_time > 0:
            keys_per_sec = self.key_count / self.active_typing_time
        else:
            keys_per_sec = 0

        # Adjusting for idle periods when calculating average time between keystrokes
        if self.key_intervals:
            avg_time_between_keystrokes = sum(self.key_intervals) / len(self.key_intervals)
        else:
            avg_time_between_keystrokes = 0

        # Reset metrics for the next interval
        self.start_time = time.time()
        self.key_count = 0
        self.char_count = 0
        self.dwell_times.clear()
        self.key_intervals.clear()
        self.active_typing_time = 0
        self.activity_flag = False
        self.last_key_time = None

        return {
            'wpm': wpm,
            'keys_per_sec': keys_per_sec,
            'avg_dwell_time': sum(self.dwell_times) / len(self.dwell_times) if self.dwell_times else 0,
            'avg_time_between_keystrokes': avg_time_between_keystrokes
        }
