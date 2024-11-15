import time

class KeystrokeMetrics:
    def __init__(self):
        self.start_time = None
        self.key_press_count = 0
        self.key_durations = []

    def start(self):
        self.start_time = time.time()
        self.key_press_count = 0
        self.key_durations = []

    def on_key_press(self):
        self.key_press_start_time = time.time()

    def on_key_release(self):
        duration = time.time() - self.key_press_start_time
        self.key_durations.append(duration)
        self.key_press_count += 1

    def stop(self):
        if self.start_time is None:
            return None
        elapsed_time = (time.time() - self.start_time) - 3  
    
        wpm = (self.key_press_count / 5) / (elapsed_time / 60)
        keys_per_second = self.key_press_count / elapsed_time
        avg_key_dwell = sum(self.key_durations) / len(self.key_durations) if self.key_durations else 0
        return {
            'wpm': wpm,
            'keys_per_sec': keys_per_second,
            'avg_dwell_time': avg_key_dwell
        }

    def reset(self):
        self.start_time = None
        self.key_press_count = 0
        self.key_durations = []
