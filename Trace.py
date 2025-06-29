import tkinter as tk
import math
import random

class EyeTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eye Tracking Exercise")
        self.canvas = tk.Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack(pady=20)

        self.instruction = tk.Label(root, text="Follow the moving circle with your eyes (not your head or mouse).")
        self.instruction.pack(pady=10)

        self.patterns = ['circle', 'sine', 'infinity']
        self.current_pattern = random.choice(self.patterns)
        self.angle = 0
        self.speed = 0.03  
        self.t = 0  

        btn = tk.Button(root, text="Change Path", command=self.change_pattern)
        btn.pack(pady=5)

        self.animate()

    def change_pattern(self):
        prev_pattern = self.current_pattern
        while True:
            self.current_pattern = random.choice(self.patterns)
            if self.current_pattern != prev_pattern:
                break
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
            x, y = 300, 150

        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="green", outline="black", width=2)
        self.canvas.create_text(300, 20, text=f"Pattern: {self.current_pattern.capitalize()}", font=("Arial", 12))


        self.angle += self.speed
        self.t += 0.03
        if self.angle > 2 * math.pi:
            self.angle = 0
        if self.t > 2 * math.pi:
            self.t = 0

        self.root.after(20, self.animate)

    def circle_path(self):
        radius = 100
        center_x = 300
        center_y = 150
        x = center_x + radius * math.cos(self.angle)
        y = center_y + radius * math.sin(self.angle)
        return x, y

    def sine_path(self):
        amplitude = 80
        freq = 2
        x = 100 + 400 * (self.t / (2 * math.pi))
        y = 150 + amplitude * math.sin(freq * self.t)
        if x > 500:
            self.t = 0
            x = 100
        return x, y

    def infinity_path(self):

        a = 120 
        center_x = 300
        center_y = 150
        t = self.angle
        x = center_x + a * math.cos(t)
        y = center_y + a * math.sin(t) * math.cos(t)
        return x, y

if __name__ == "__main__":
    root = tk.Tk()
    app = EyeTrackingApp(root)
    root.mainloop()