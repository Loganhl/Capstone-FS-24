from pynput import *
#these will need to be modified to add what to do when someone presses a key
def on_press(key):
    pressed = {}
    try:
        print('key: {0} pressed '.format(key.char))
        pressed.add('{0}'.format(key.char))
        
    except AttributeError:
        print('special key {0} pressed'.format(key))
        
def on_release(key):
    print('{0}  released'.format(key))