import time
from pynput.mouse import Listener

class MouseMetrics:
    MIN_MOVEMENTS = 3  # minimum movements to calculate metrics
    MOVEMENT_THRESHOLD = 5 #minimum amount of pixels for a valid mouse movement
    EMA_ALPHA = 0.1

    #initialize variables
    def __init__(self):
        self.start_time = None
        self.click_durations = []
        self.click_start_time = None
        self.distance_moved = 0
        self.last_position = None
        self.last_time = None
        self.time_moving = 0
        self.ema_speed = 0
        self.movement_count = 0

    def start(self):
        self.start_time = time.time()
        self.click_durations = []
        self.distance_moved = 0
        self.last_position = None
        self.last_time = None
        self.time_moving = 0
        self.ema_speed = 0
        self.movement_count = 0


    
    #Track time of click and append it 
    def on_click(self, x, y , button, pressed):
        if pressed:
            self.click_start_time = time.time()
        else:
            if self.click_start_time:
                duration = time.time() - self.click_start_time
                self.click_durations.append(duration)


    def on_move(self, x, y):
        current_time = time.time()
        if self.last_position is not None:
            dx = x - self.last_position[0]
            dy = y - self.last_position[1]
            distance = (dx**2 + dy**2) ** 0.5

            if distance > self.MOVEMENT_THRESHOLD:
                time_delta = current_time - self.last_time if self.last_time else 0
                if time_delta > 0:
                    instant_speed = distance / time_delta
                    # Update EMA speed
                    self.ema_speed = (self.EMA_ALPHA * instant_speed) + ((1 - self.EMA_ALPHA) * self.ema_speed)

                    self.distance_moved += distance
                    self.time_moving += time_delta
                    self.movement_count +=1


        self.last_position = (x, y)
        self.last_time = current_time
        

    #stops session and returns values
    def stop(self, is_switch=False):
        print(self.movement_count)
        if self.start_time is None or self.movement_count < self.MIN_MOVEMENTS:
            print(f"Insufficient movements: {self.movement_count}")
            return None

        elapsed_time = time.time() - self.start_time
        if is_switch:
            elapsed_time -= 3

        avg_click_dwell = sum(self.click_durations) / len(self.click_durations) if self.click_durations else 0

        return {
            'avg_click_dwell_time': avg_click_dwell,
            'mouse_speed': self.ema_speed
        }

    def reset(self):
        self.start_time = None
        self.click_durations = []
        self.distance_moved = 0
        self.last_position = None
        self.last_time = None
        self.time_moving = 0
        self.ema_speed = 0
        self.movement_count = 0
