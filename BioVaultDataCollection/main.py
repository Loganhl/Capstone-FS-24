
import time
from metrics.keystroke_metrics import KeystrokeMetrics
from metrics.mouse_metrics import MouseMetrics
from database.database import Database
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
from metrics.session_manager import SessionManager



def main():
    db = Database()
    session_manager = SessionManager(db)
    

    def on_key_press(key):
        session_manager.start_keyboard_session()
        session_manager.keyboard_metrics.on_key_press()
        session_manager.update_activity()

    def on_key_release(key):
        session_manager.keyboard_metrics.on_key_release()
        session_manager.update_activity()

    def on_move(x, y):
        session_manager.start_mouse_session()
        session_manager.mouse_metrics.on_move(x, y)
        session_manager.update_activity()

    def on_click(x, y, button, pressed):
        session_manager.start_mouse_session()
        session_manager.mouse_metrics.on_click(x, y, button, pressed)
        session_manager.update_activity()

    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    mouse_listener = MouseListener(on_move=on_move, on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    try:
        while True:
            session_manager.check_inactivity()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping program...")
    finally:
        db.close()


if __name__ == "__main__":
    main()