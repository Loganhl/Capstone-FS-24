import time
from metrics.keystroke_metrics import KeystrokeMetrics
from metrics.mouse_metrics import MouseMetrics
from kc import get_userid
from database.database import Database
INACTIVITY_TIMEOUT = 3

class SessionManager:
    def __init__(self, db):
        self.db = db
        self.keyboard_metrics = KeystrokeMetrics()
        self.mouse_metrics = MouseMetrics()
        self.current_session = None
        self.last_activity_time = time.time()

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
        user_id = get_userid('user@user.com', 'user')
        if self.current_session == 'keyboard':
            metrics = self.keyboard_metrics.stop()
            if metrics and metrics['wpm'] > 0:
                self.db.insert_metric('wpm', metrics['wpm'], user_id)
                self.db.insert_metric('keys_per_sec', metrics['keys_per_sec'], user_id)
                self.db.insert_metric('avg_dwell_time', metrics['avg_dwell_time'], user_id)
            self.keyboard_metrics.reset()
        elif self.current_session == 'mouse':
            metrics = self.mouse_metrics.stop()
            if metrics and metrics['avg_click_dwell_time'] > 0:
                self.db.insert_metric('avg_click_dwell_time', metrics['avg_click_dwell_time'], user_id)
                self.db.insert_metric('mouse_speed', metrics['mouse_speed'], user_id)
            self.mouse_metrics.reset()
        self.current_session = None

    def check_inactivity(self):
        if time.time() - self.last_activity_time >= INACTIVITY_TIMEOUT:
            self.end_session()

    def update_activity(self):
        self.last_activity_time = time.time()