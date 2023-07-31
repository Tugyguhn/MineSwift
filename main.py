import tkinter as tk
from pynput.mouse import Controller, Button
from pynput import keyboard
import threading
import time

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MineSwift")
        self.root.geometry("400x300")
        self.root.resizable(False, False)  # Make the window non-resizable

        # Add a dark background
        self.background_image = tk.PhotoImage(file="background.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(root, text="MineSwift", font=("Helvetica", 24), fg="white", bg="#151618")
        self.label.pack(pady=10)

        self.click_speed = 10

        self.click_label = tk.Label(root, text=f"Clicks per second: {self.click_speed}", fg="white", bg="#151618")
        self.click_label.pack(pady=5)

        self.slider = tk.Scale(root, from_=1, to=20, orient="horizontal", command=self.update_speed, bg="#151618", fg="white", highlightthickness=0)
        self.slider.pack()

        self.is_clicking = False
        self.toggle_button = tk.Button(root, text="Start", command=self.toggle_click, fg="white", bg="#151618")
        self.toggle_button.pack(pady=10)

        self.keybind_label = tk.Label(root, text="Press 'Set Keybind' to choose a key for the auto clicker", fg="white", bg="#151618")
        self.keybind_label.pack(pady=5)

        self.set_keybind_button = tk.Button(root, text="Set Keybind", command=self.bind_key, fg="white", bg="#151618")
        self.set_keybind_button.pack(pady=5)

        self.selected_keybind_label = tk.Label(root, text="Selected Keybind: None", fg="white", bg="#151618")
        self.selected_keybind_label.pack(pady=5)

        self.keybind = None
        self.listener = None  # Initialize listener with None
        self.listener_thread = threading.Thread(target=self.listen_keybind)
        self.listener_thread.start()

        # Add Always On Top Button
        self.always_on_top_button = tk.Button(root, text="Always On Top: Off", command=self.toggle_always_on_top, fg="white", bg="#151618")
        self.always_on_top_button.pack(pady=5)

    def update_speed(self, value):
        self.click_speed = int(value)
        self.click_label.config(text=f"Clicks per second: {self.click_speed}")

    def on_press(self, key):
        try:
            if key.char == self.keybind:
                self.toggle_click()
        except AttributeError:
            pass

    def bind_key(self):
        self.set_keybind_button.config(text="Press a Key")
        self.root.bind("<KeyPress>", self.on_key_press)

    def on_key_press(self, event):
        self.set_keybind_button.config(text="Set Keybind")
        self.keybind = event.char
        self.root.unbind("<KeyPress>")
        if self.listener:
            self.listener.stop()
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.selected_keybind_label.config(text=f"Selected Keybind: {self.keybind}")

    def toggle_click(self):
        if not self.is_clicking:
            self.is_clicking = True
            self.toggle_button.config(text="Stop")
            threading.Thread(target=self.click).start()
        else:
            self.is_clicking = False
            self.toggle_button.config(text="Start")

    def click(self):
        mouse = Controller()
        while self.is_clicking:
            if self.click_speed > 0:
                mouse.press(Button.left)
                time.sleep(1.0 / self.click_speed)
                mouse.release(Button.left)
            else:
                break

    def listen_keybind(self):
        while True:
            time.sleep(0.1)  # Check for keybind changes every 0.1 seconds

    def toggle_always_on_top(self):
        if not self.root.attributes("-topmost"):
            self.root.attributes("-topmost", True)
            self.always_on_top_button.config(text="Always On Top: On")
        else:
            self.root.attributes("-topmost", False)
            self.always_on_top_button.config(text="Always On Top: Off")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
