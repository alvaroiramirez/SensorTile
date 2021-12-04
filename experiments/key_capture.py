from pynput.keyboard import Key, Listener

currently_pressed_key = None

def on_press(key):
    global currently_pressed_key
    if key == currently_pressed_key:
        print('{0} repeated'.format(key))
    else:
        print('{0} pressed'.format(key))
        currently_pressed_key = key

def on_release(key):
    global currently_pressed_key
    print('{0} release'.format(key))
    currently_pressed_key = None
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()