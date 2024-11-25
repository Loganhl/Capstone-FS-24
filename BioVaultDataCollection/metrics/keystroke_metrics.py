import time

class KeystrokeMetrics:

    #threashold for calculations
    MIN_KEY_PRESSES = 10

    def __init__(self):
        self.start_time = None
        self.key_press_count = 0
        self.key_durations = []
        self.key_release_times = []

    def start(self):
        self.start_time = time.time()
        self.key_press_count = 0
        self.key_durations = []
        self.key_release_times = []


    #tracks key press time
    def on_key_press(self):
        self.key_press_start_time = time.time()

    #tracks key release time and duration of the key press
    def on_key_release(self):
        if self.key_press_start_time is None:
            return
        release_time = time.time()
        duration = release_time - self.key_press_start_time
        self.key_durations.append(duration)
        self.key_press_count += 1
        self.key_release_times.append(release_time)

    #stops session and returns values
    def stop(self, is_switch=False):
        if self.start_time is None or self.key_press_count < self.MIN_KEY_PRESSES:
            print(f"Insufficient key presses: {self.key_press_count}")
            return None

        elapsed_time = time.time() - self.start_time
        if is_switch:
            elapsed_time -= 3

        intervals = [
            self.key_release_times[i] - self.key_release_times[i - 1]
            for i in range(1, len(self.key_release_times))
        ]

        wpm = (self.key_press_count / 5) / (elapsed_time / 60)
        keys_per_second = self.key_press_count / elapsed_time
        avg_key_dwell = sum(self.key_durations) / len(self.key_durations) if self.key_durations else 0
        avg_time_between_keystrokes = sum(intervals) / len(intervals) if intervals else 0

        return {
            'wpm': wpm,
            'keys_per_sec': keys_per_second,
            'avg_dwell_time': avg_key_dwell,
            'avg_time_between_keystrokes': avg_time_between_keystrokes
        }

    def reset(self):
        self.start_time = None
        self.key_press_count = 0
        self.key_durations = []
        self.key_release_times = []
