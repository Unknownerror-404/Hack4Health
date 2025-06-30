import tkinter as tk
import math
import random

class EyeTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Tracking Exercise")
        self.root.geometry("900x600")
        self.root.option_add("*Font", "Arial 14")

        self.current_theme = "light"

        self.light_theme = {
            "bg": "#f2f6f9", "fg": "#222222", "circle": "#28a745",
            "text": "#222", "btn_bg": "#cfe2f3", "btn_fg": "black"
        }
        self.dark_theme = {
            "bg": "#121212", "fg": "#eeeeee", "circle": "#33ff33",
            "text": "#eee", "btn_bg": "#333333", "btn_fg": "white"
        }

        self.set_theme_colors()

        # Canvas
        self.canvas = tk.Canvas(self.root, width=850, height=400, bg=self.theme_colors["bg"], highlightthickness=0)
        self.canvas.pack(pady=20)

        # Instruction
        self.instruction = tk.Label(
            self.root,
            text="👁️Follow the moving dot with your eyes from about 50 cm away.",
            bg=self.theme_colors["bg"],
            fg=self.theme_colors["fg"],
            wraplength=780,
            justify="center"
        )
        self.instruction.pack(pady=(0, 15))

        # Change Path Button
        self.change_btn = tk.Button(
            self.root,
            text="🔄 Change Path",
            command=self.change_pattern,
            bg=self.theme_colors["btn_bg"],
            fg=self.theme_colors["btn_fg"],
            relief="flat",
            padx=10,
            pady=5
        )
        self.change_btn.pack(pady=5)

        # Theme Toggle Button
        self.theme_btn = tk.Button(
            self.root,
            text="🌓",
            command=self.toggle_theme,
            bg=self.theme_colors["btn_bg"],
            fg=self.theme_colors["btn_fg"],
            font=("Arial", 10),
            relief="flat",
            width=3,
            height=1
        )
        self.theme_btn.place(relx=0.98, rely=0.02, anchor="ne")

        # Animation state
        self.patterns = ['circle', 'sine', 'infinity']
        self.current_pattern = random.choice(self.patterns)
        self.angle = 0
        self.speed = 0.03
        self.t = 0

        self.animate()

    def set_theme_colors(self):
        self.theme_colors = self.dark_theme if self.current_theme == "dark" else self.light_theme

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.set_theme_colors()
        self.update_theme()

    def update_theme(self):
        self.root.config(bg=self.theme_colors["bg"])
        self.canvas.config(bg=self.theme_colors["bg"])
        self.instruction.config(bg=self.theme_colors["bg"], fg=self.theme_colors["fg"])
        self.change_btn.config(bg=self.theme_colors["btn_bg"], fg=self.theme_colors["btn_fg"])
        self.theme_btn.config(bg=self.theme_colors["btn_bg"], fg=self.theme_colors["btn_fg"])

    def change_pattern(self):
        prev = self.current_pattern
        while self.current_pattern == prev:
            self.current_pattern = random.choice(self.patterns)
        self.angle = 0
        self.t = 0

    def animate(self):
        self.canvas.delete("all")

        if self.current_pattern == 'circle':
            x, y = self.circle_path()
        elif self.current_pattern == 'sine':
            x, y = self.sine_path()
        elif self.current_pattern == 'infinity':
            x, y = self.infinity_path()
        else:
            x, y = 450, 250

        self.canvas.create_oval(
            x - 20, y - 20, x + 20, y + 20,
            fill=self.theme_colors["circle"],
            outline=self.theme_colors["fg"],
            width=2
        )
        self.canvas.create_text(
            430, 20,
            text=f"Pattern: {self.current_pattern.capitalize()}",
            font=("Arial", 12),
            fill=self.theme_colors["text"]
        )

        self.angle += self.speed
        self.t += 0.03
        self.angle %= 2 * math.pi
        self.t %= 2 * math.pi

        self.root.after(20, self.animate)

    def circle_path(self):
        r = 150
        cx, cy = 425, 200
        x = cx + r * math.cos(self.angle)
        y = cy + r * math.sin(self.angle)
        return x, y

    def sine_path(self):
        amp = 100
        freq = 2
        x = 100 + 700 * (self.t / (2 * math.pi))
        y = 200 + amp * math.sin(freq * self.t)
        if x > 800:
            self.t = 0
            x = 100
        return x, y

    def infinity_path(self):
        a = 160
        cx, cy = 425, 200
        t = self.angle
        x = cx + a * math.cos(t)
        y = cy + a * math.sin(t) * math.cos(t)
        return x, y


def launch_eye_tracking_app():
    root = tk.Tk()
    EyeTrackingApp(root)
    root.mainloop()
