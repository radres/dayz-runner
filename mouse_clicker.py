from pynput import keyboard
import pydirectinput
import time
import threading

class MouseClicker:
    def __init__(self):
        self.active = False
        self.stop_event = threading.Event()
        # Setup listener for keypresses
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.click_thread = None

    def on_key_press(self, key):
        try:
            if key.char == '/' or key.char == "?":  # Toggle with '/'
                self.toggle_clicking()
            elif key == keyboard.Key.esc:  # Exit on 'esc'
                self.cleanup_and_exit()
        except AttributeError:
            pass

    def toggle_clicking(self):
        if self.active:
            print("Stopping auto-clicking")
            self.active = False
            self.stop_event.set()
        else:
            print("Starting auto-clicking every 5 seconds")
            self.active = True
            self.stop_event.clear()
            self.click_thread = threading.Thread(target=self.click_loop)
            self.click_thread.daemon = True
            self.click_thread.start()

    def click_loop(self):
        while self.active and not self.stop_event.is_set():
            print("Clicking mouse")
            pydirectinput.click()
            
            # Wait 5 seconds before next click
            for _ in range(5):
                if self.stop_event.is_set():
                    return
                time.sleep(1)

    def cleanup_and_exit(self):
        print("Cleaning up...")
        self.active = False
        self.stop_event.set()
        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join(timeout=1)
        self.listener.stop()
        print("Exiting...")
        exit(0)

# Main logic
if __name__ == "__main__":
    clicker = MouseClicker()
    print("Press '/' to toggle mouse clicking every 5 seconds, 'Esc' to exit.")
    clicker.listener.join()  # Keep the program running to listen for keypresses 