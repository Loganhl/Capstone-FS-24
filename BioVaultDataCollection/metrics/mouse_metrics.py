import time
from pynput.mouse import Listener

class MouseMetrics:
    def __init__(self):
        self.start_time = None
        self.click_durations = []
        self.click_start_time = None
        self.distance_moved = 0
        self.last_position = None

    def start(self):
        self.start_time = time.time()
        self.click_durations = []
        self.distance_moved = 0
        self.last_position = None

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_start_time = time.time()
        else:
            if self.click_start_time:
                duration = time.time() - self.click_start_time
                self.click_durations.append(duration)

    def on_move(self, x, y):
        if self.last_position is not None:
            dx = x - self.last_position[0]
            dy = y - self.last_position[1]
            self.distance_moved += (dx**2 + dy**2) ** 0.5
        self.last_position = (x, y)

    def stop(self):
        if self.start_time is None:
            return None
        elapsed_time = (time.time() - self.start_time) - 3
        avg_click_dwell = sum(self.click_durations) / len(self.click_durations) if self.click_durations else 0
        mouse_speed = self.distance_moved / elapsed_time if elapsed_time > 0 else 0
        return {
            'avg_click_dwell_time': avg_click_dwell,
            'mouse_speed': mouse_speed
        }

    def reset(self):
        self.start_time = None
        self.click_durations = []
        self.distance_moved = 0
        self.last_position = None
