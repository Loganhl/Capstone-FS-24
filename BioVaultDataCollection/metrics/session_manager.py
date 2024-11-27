import time
from metrics.keystroke_metrics import KeystrokeMetrics
from metrics.mouse_metrics import MouseMetrics
from database.database import Database
INACTIVITY_TIMEOUT = 2

class SessionManager:

    #initialize variable
    def __init__(self, db,user_id):
        self.db = db
        self.keyboard_metrics = KeystrokeMetrics()
        self.mouse_metrics = MouseMetrics()
        self.current_session = None
        self.last_activity_time = time.time()
        self.user_id = user_id

    #start keyboard session if there is not one already going on
    def start_keyboard_session(self):
        if self.current_session != 'keyboard':
            print("Starting keyboard session...")
            self.end_session()
            self.keyboard_metrics.start()
            self.current_session = 'keyboard'


    #start mouse session if there is not one already going on
    def start_mouse_session(self):
        if self.current_session != 'mouse':
            print("Starting mouse session...")
            self.end_session()
            self.mouse_metrics.start()
            self.current_session = 'mouse'


    #stop current session and insert 
    def end_session(self):
        if self.current_session == 'keyboard':
            metrics = self.keyboard_metrics.stop()
            if metrics and metrics['wpm'] > 0:
                self.db.insert_metric('wpm', metrics['wpm'], self.user_id)
                self.db.insert_metric('keys_per_sec', metrics['keys_per_sec'], self.user_id)
                self.db.insert_metric('avg_dwell_time', metrics['avg_dwell_time'], self.user_id)
                self.db.insert_metric('avg_time_between_keystrokes', metrics['avg_time_between_keystrokes'], self.user_id)
            self.keyboard_metrics.reset()
        elif self.current_session == 'mouse':
            metrics = self.mouse_metrics.stop()
            if metrics and 20000 > metrics['mouse_speed'] > 0:
                self.db.insert_metric('avg_click_dwell_time', metrics['avg_click_dwell_time'], self.user_id)
                self.db.insert_metric('mouse_speed', metrics['mouse_speed'], self.user_id)
            self.mouse_metrics.reset()
        self.current_session = None


    #if a user is not active for 3 seconds the session ends
    def check_inactivity(self):
        if time.time() - self.last_activity_time >= INACTIVITY_TIMEOUT:
            self.end_session()

    #updates last activity time
    def update_activity(self):
        self.last_activity_time = time.time()

