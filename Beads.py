import tkinter as tk
import random

class BrockStringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brock String (Beads Concentration) Exercise")
        self.canvas = tk.Canvas(root, width=600, height=200, bg="white")
        self.canvas.pack(pady=20)

        self.num_beads = 5
        self.focus_index = random.randint(0, self.num_beads - 1)
        self.bead_positions = [100, 200, 300, 400, 500]  # Stationary beads

        self.draw_string_and_beads()

        self.instruction = tk.Label(root, text="Click the highlighted bead to progress.")
        self.instruction.pack(pady=10)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_string_and_beads(self):
        self.canvas.delete("all")
        # Draw the string
        self.canvas.create_line(80, 100, 520, 100, width=4, fill="brown")
        # Draw beads
        self.bead_coords = []
        for i, x in enumerate(self.bead_positions):
            color = "red" if i == self.focus_index else "gray"
            self.canvas.create_oval(x-20, 80, x+20, 120, fill=color, outline="black", width=2)
            self.canvas.create_text(x, 130, text=f"Bead {i+1}")
            self.bead_coords.append((x-20, 80, x+20, 120))  # Store bead bounding box

    def on_canvas_click(self, event):
        # Check if click is inside the focused bead
        x1, y1, x2, y2 = self.bead_coords[self.focus_index]
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            # Move focus to a random bead that's not the current one
            possible_indices = [i for i in range(self.num_beads) if i != self.focus_index]
            if possible_indices:
                self.focus_index = random.choice(possible_indices)
                self.draw_string_and_beads()
            else:
                self.instruction.config(text="Exercise complete! Restarting...")
                self.root.after(1500, self.reset_exercise)

    def reset_exercise(self):
        self.instruction.config(text="Click the highlighted bead to progress.")
        self.focus_index = random.randint(0, self.num_beads - 1)
        self.draw_string_and_beads()

if __name__ == "__main__":
    root = tk.Tk()
    app = BrockStringApp(root)
    root.mainloop()