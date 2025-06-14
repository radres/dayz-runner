from pynput import keyboard
import subprocess
import os

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
            subprocess.run(['xdotool', 'keyup', 'shift'], check=False)
            subprocess.run(['xdotool', 'keyup', 'w'], check=False)
        else:
            print("Starting run")
            self.running = True
            subprocess.run(['xdotool', 'keydown', 'shift'], check=False)
            subprocess.run(['xdotool', 'keydown', 'w'], check=False)

    def cleanup_and_exit(self):
        print("Cleaning up...")
        if self.running:
            subprocess.run(['xdotool', 'keyup', 'shift'], check=False)
            subprocess.run(['xdotool', 'keyup', 'w'], check=False)
        self.listener.stop()  # Stop the key listener
        print("Exiting...")
        exit(0)

# Main logic
if __name__ == "__main__":
    runner = DayZRunner(window_name="DayZ")
    print("Press '/' to toggle running, 'Esc' to exit.")
    runner.listener.join()  # Keep the program running to listen for keypresses
