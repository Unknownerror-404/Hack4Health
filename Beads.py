import tkinter as tk
import random

class BrockStringApp:
    def __init__(self, root, direction="horizontal", on_complete=None, total_rounds=None):
        self.root = root
        self.root.title("Brock String (Beads Concentration) Exercise")
        self.root.geometry("650x300")
        self.direction = direction
        self.on_complete = on_complete
        self.total_rounds = total_rounds or random.randint(3, 20)
        self.current_round = 1
        self.current_theme = "light"

        self.light_theme = {
            "bg": "#ffffff", "canvas_bg": "#f2f2f2", "instruction": "#000000",
            "button_bg": "#dddddd", "button_fg": "#000000",
            "bead": "#4287f5", "focus_bead": "#ff4444", "string": "#000000", "text": "#000000"
        }
        self.dark_theme = {
            "bg": "#121212", "canvas_bg": "#1e1e1e", "instruction": "#ffffff",
            "button_bg": "#333333", "button_fg": "#ffffff",
            "bead": "#3a86ff", "focus_bead": "#ff006e", "string": "#ffffff", "text": "#ffffff"
        }

        self.num_beads = 5
        self.clicked_beads = set()
        self.bead_coords = []
        self.focus_index = None

        self.canvas = tk.Canvas(root, width=600, height=200)
        self.canvas.pack(pady=20)

        self.instruction = tk.Label(root, text="", font=("Arial", 18))
        self.instruction.pack(pady=5)

        self.toggle_button = tk.Button(
            root, text="🌓", command=self.toggle_theme,
            relief="flat", font=("Arial", 10), width=3, height=1
        )
        self.toggle_button.place(relx=1.0, x=-40, y=10, anchor="ne")

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.initialize_beads()
        self.pick_next_bead()
        self.apply_theme()

    def get_theme(self):
        return self.dark_theme if self.current_theme == "dark" else self.light_theme

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        theme = self.get_theme()
        self.root.configure(bg=theme["bg"])
        self.canvas.configure(bg=theme["canvas_bg"])
        self.instruction.configure(bg=theme["bg"], fg=theme["instruction"])
        self.toggle_button.configure(bg=theme["button_bg"], fg=theme["button_fg"])
        self.redraw_beads()

    def initialize_beads(self):
        self.bead_coords = []
        if self.direction == "vertical":
            positions = [60, 100, 140, 180, 220]
            for y in positions:
                self.bead_coords.append((280, y - 20, 320, y + 20))
        else:
            positions = [100, 200, 300, 400, 500]
            for x in positions:
                self.bead_coords.append((x - 20, 80, x + 20, 120))

    def redraw_beads(self):
        theme = self.get_theme()
        self.canvas.delete("all")

        if self.direction == "vertical":
            self.canvas.create_line(300, 60, 300, 220, width=4, fill=theme["string"])
            for i, (x1, y1, x2, y2) in enumerate(self.bead_coords):
                fill = theme["focus_bead"] if i == self.focus_index else theme["bead"]
                self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline="black", width=2)
                self.canvas.create_text(300, y2 + 10, text=f"Bead {i + 1}", fill=theme["text"], font=("Arial", 14))
        else:
            self.canvas.create_line(80, 100, 520, 100, width=4, fill=theme["string"])
            for i, (x1, y1, x2, y2) in enumerate(self.bead_coords):
                fill = theme["focus_bead"] if i == self.focus_index else theme["bead"]
                self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline="black", width=2)
                self.canvas.create_text(x1 + 20, y2 + 10, text=f"Bead {i + 1}", fill=theme["text"], font=("Arial", 14))

        self.instruction.config(
            text=f"Round {self.current_round}/{self.total_rounds} — Click the highlighted bead."
        )

    def pick_next_bead(self):
        remaining = set(range(self.num_beads)) - self.clicked_beads
        if remaining:
            self.focus_index = random.choice(list(remaining))
            self.redraw_beads()
        else:
            self.current_round += 1
            if self.current_round > self.total_rounds:
                self.instruction.config(text="✅ Exercise complete!")
                self.root.after(1000, self.close_app)
            else:
                self.clicked_beads.clear()
                self.focus_index = None
                self.pick_next_bead()

    def on_canvas_click(self, event):
        if self.focus_index is None or self.focus_index >= len(self.bead_coords):
            return
        x1, y1, x2, y2 = self.bead_coords[self.focus_index]
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            self.clicked_beads.add(self.focus_index)
            self.pick_next_bead()

    def close_app(self):
        self.root.destroy()
        if self.on_complete:
            self.on_complete()

def launch_brock_string_app(direction="horizontal", on_complete=None, total_rounds=None):
    root = tk.Tk()
    BrockStringApp(root, direction=direction, on_complete=on_complete, total_rounds=total_rounds)
    root.mainloop()
