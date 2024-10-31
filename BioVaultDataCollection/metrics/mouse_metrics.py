import time
from pynput import mouse

class MouseMetrics:
    def __init__(self, interval_duration=10):
        self.interval_duration = interval_duration
        self.start_time = time.time()
        self.activity_time = 0
        self.move_count = 0
        self.click_count = 0
        self.click_durations = []
        self.last_move_time = None
        self.activity_flag = False

        # Start mouse listener
        self.listener = mouse.Listener(
            on_click=self.on_click,
            on_move=self.on_move
        )
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        current_time = time.time()
        if pressed:
            self.click_start_time = current_time
        else:
            if hasattr(self, 'click_start_time'):
                dwell_time = current_time - self.click_start_time
                self.click_durations.append(dwell_time)
                self.click_count += 1
                self.activity_flag = True
                del self.click_start_time

    def on_move(self, x, y):
        current_time = time.time()
        if self.last_move_time:
            self.activity_time += current_time - self.last_move_time
        self.move_count += 1
        self.last_move_time = current_time
        self.activity_flag = True

    def calculate_metrics(self):
        movement_ratio = self.activity_time / self.interval_duration if self.activity_time > 0 else 1
        mouse_speed = (self.move_count / self.interval_duration) / movement_ratio
        avg_click_dwell_time = sum(self.click_durations) / len(self.click_durations) if self.click_durations else 0

        # Reset metrics
        self.start_time = time.time()
        self.move_count = 0
        self.click_count = 0
        self.click_durations.clear()
        self.activity_time = 0
        self.activity_flag = False

        return {
            'mouse_speed': mouse_speed,
            'avg_click_dwell_time': avg_click_dwell_time
        }
