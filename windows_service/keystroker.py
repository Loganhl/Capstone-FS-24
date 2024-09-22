from pynput import *

def on_press(key):
    try:
        print('key: {0} pressed '.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))
        
def on_release(key):
    print('{0}  released'.format(key))