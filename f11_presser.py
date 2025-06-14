from pynput import keyboard
import pydirectinput
import time
import threading

class F11Presser:
    def __init__(self):
        self.active = False
        self.stop_event = threading.Event()
        # Setup listener for keypresses
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.press_thread = None

    def on_key_press(self, key):
        try:
            if key.char == '/' or key.char == "?":  # Toggle with '/'
                self.toggle_pressing()
            elif key == keyboard.Key.esc:  # Exit on 'esc'
                self.cleanup_and_exit()
        except AttributeError:
            pass

    def toggle_pressing(self):
        if self.active:
            print("Stopping sequence")
            self.active = False
            self.stop_event.set()
        else:
            print("Starting sequence")
            self.active = True
            self.stop_event.clear()
            self.press_thread = threading.Thread(target=self.action_sequence)
            self.press_thread.daemon = True
            self.press_thread.start()

    def action_sequence(self):
        while self.active and not self.stop_event.is_set():
            # Step 1: Press F11
            print("Pressing F11")
            pydirectinput.press('f11')
            
            # Step 2: Wait 15 seconds
            print("Waiting 15 seconds...")
            for _ in range(15):
                if self.stop_event.is_set():
                    return
                time.sleep(1)
            
            # Step 3: Click mouse
            print("Clicking mouse")
            pydirectinput.click()
            
            # Step 4: Wait 5 seconds
            print("Waiting 5 seconds...")
            for _ in range(5):
                if self.stop_event.is_set():
                    return
                time.sleep(1)
            
            # Step 5: Press ESC
            print("Pressing ESC")
            pydirectinput.press('esc')
            
            # Optional: Small pause before starting the next cycle
            time.sleep(1)

    def cleanup_and_exit(self):
        print("Cleaning up...")
        self.active = False
        self.stop_event.set()
        if self.press_thread and self.press_thread.is_alive():
            self.press_thread.join(timeout=1)
        self.listener.stop()
        print("Exiting...")
        exit(0)

# Main logic
if __name__ == "__main__":
    presser = F11Presser()
    print("Press '/' to toggle sequence (F11 → wait 15s → mouse click → wait 5s → ESC), 'Esc' to exit.")
    presser.listener.join()  # Keep the program running to listen for keypresses 