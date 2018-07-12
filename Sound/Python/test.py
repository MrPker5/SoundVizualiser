from pynput.keyboard import Key, Listener
from pynput import keyboard

def on_press(key):
    key_name = get_key_name(key)
    print('Key {} pressed.'.format(key_name))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)
 

# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()