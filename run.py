from pynput import keyboard
import pydirectinput

class DayZRunner:
    def __init__(self, window_name):
        self.running = False
        # Setup listener for keypresses
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.press_count = 0

    def on_key_press(self, key):
        print(key)
        print(type(key))
        # Check if the key is the '/' key and Shift is also pressed
        if self.press_count > 50:
            self.cleanup_and_exit()
        try:
            if key.char == '/' or key.char == "?":  # Toggle on '/'
                self.toggle_run()
            elif key == keyboard.Key.esc:  # Exit on 'esc'
                self.cleanup_and_exit()
        except AttributeError:
            pass

    def toggle_run(self):
        if self.running:
            print("Stopping run")
            self.running = False
            pydirectinput.keyUp('shift')  # Release Shift
            pydirectinput.keyUp('w')  # Release W
        else:
            print("Starting run")
            self.running = True
            pydirectinput.keyDown('shift')  # Press Shift
            pydirectinput.keyDown('w')  # Press W

    def cleanup_and_exit(self):
        print("Cleaning up...")
        if self.running:
            pydirectinput.keyUp('shift')  # Ensure Shift is released
            pydirectinput.keyUp('w')  # Ensure W is released
        self.listener.stop()  # Stop the key listener
        print("Exiting...")
        exit(0)

# Main logic
if __name__ == "__main__":
    runner = DayZRunner(window_name="DayZ")
    print("Press '/' to toggle running, 'Esc' to exit.")
    runner.listener.join()  # Keep the program running to listen for keypresses
