from pynput import keyboard

error_count = 0

def on_press(key):
    global error_count
    try: 
        if key == keyboard.Key.backspace:
            error_count += 1

    except AttributeError:
        pass

def get_error_count():
    return error_count

