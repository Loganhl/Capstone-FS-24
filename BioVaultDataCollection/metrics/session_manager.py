import time
from metrics.keystroke_metrics import KeystrokeMetrics
from metrics.mouse_metrics import MouseMetrics
from database.database import Database

INACTIVITY_TIMEOUT = 2


class SessionManager:
    def __init__(self, db, user_id):
        self.db = db
        self.keyboard_metrics = KeystrokeMetrics()
        self.mouse_metrics = MouseMetrics()
        self.current_session = None
        self.last_activity_time = time.time()
        self.user_id = user_id
        self.use_training_tables = True

    def start_keyboard_session(self):
        if self.current_session != 'keyboard':
            print("Starting keyboard session...")
            self.end_session()
            self.keyboard_metrics.start()
            self.current_session = 'keyboard'

    def start_mouse_session(self):
        if self.current_session != 'mouse':
            print("Starting mouse session...")
            self.end_session()
            self.mouse_metrics.start()
            self.current_session = 'mouse'

    def end_session(self): 
        if self.current_session == 'keyboard':
            metrics = self.keyboard_metrics.stop()
            if metrics and metrics['wpm'] > 0:
                if self.use_training_tables:
                    keystroke_metrics = {
                        'wpm': metrics['wpm'],
                        'keys_per_sec': metrics['keys_per_sec'],
                        'avg_dwell_time': metrics['avg_dwell_time'],
                        'avg_time_between_keystrokes': metrics['avg_time_between_keystrokes']
                    }
                    self.db.insert_metrics('keystroke_training_data', keystroke_metrics, self.user_id)
                else:
                    self.db.insert_regular_metric('wpm', metrics['wpm'], self.user_id)
                    self.db.insert_regular_metric('keys_per_sec', metrics['keys_per_sec'], self.user_id)
                    self.db.insert_regular_metric('avg_dwell_time', metrics['avg_dwell_time'], self.user_id)
                    self.db.insert_regular_metric('avg_time_between_keystrokes', metrics['avg_time_between_keystrokes'], self.user_id)
            self.keyboard_metrics.reset()
        elif self.current_session == 'mouse':
            metrics = self.mouse_metrics.stop()
            if metrics and 20000 > metrics['mouse_speed'] > 0:
                if self.use_training_tables:
                    mouse_metrics = {
                        'avg_click_dwell_time': metrics['avg_click_dwell_time'],
                        'mouse_speed': metrics['mouse_speed']
                    }
                    self.db.insert_metrics('mouse_training_data', mouse_metrics, self.user_id)
                else:
                    self.db.insert_regular_metric('avg_click_dwell_time', metrics['avg_click_dwell_time'], self.user_id)
                    self.db.insert_regular_metric('mouse_speed', metrics['mouse_speed'], self.user_id)
            self.mouse_metrics.reset()
        self.current_session = None


    def check_inactivity(self):
        if time.time() - self.last_activity_time >= INACTIVITY_TIMEOUT:
            self.end_session()

    def update_activity(self):
        self.last_activity_time = time.time()

    def check_training_tables(self):
        if self.use_training_tables:
            training_complete = self.db.check_training_data_complete(self.user_id)
            if training_complete:
                print("Training data complete. Switching to regular metric tables.")
                self.use_training_tables = False
