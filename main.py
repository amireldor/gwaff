# I'm trying to make a graph-like "database" editor
import tkinter as tk


class World():
    def __init__(self):
        self.circles = []

    def add_circle(self, x, y):
        self.circles += [{
            "position": (x, y),
        }]

    def find_circle(self, x, y):
        search_distance = 50
        for index, circle in enumerate(self.circles):
            if abs(circle['position'][0] - x) < search_distance and \
               abs(circle['position'][1] - y) < search_distance:
                return circle
        return None


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.world = World()

        self.update()
        width, height = self.master.winfo_width(), self.master.winfo_height()
        self.canvas = None
        self.create_widgets(width, height)
        self.bind_events()

    def create_widgets(self, width, height):
        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.canvas.pack()

    def bind_events(self):
        self.master.bind("<Button-1>", self.mouse_left_click)

    def mouse_left_click(self, event):
        x, y = event.x, event.y
        circle = self.world.find_circle(x, y)
        if circle:
            x, y = circle['position'][0], circle['position'][1]
            dimensions = [x-15, y-15, x+15, y+15]
            self.canvas.create_oval(*dimensions, fill="#42ffbd")
        else:
            dimensions = [x-15, y-15, x+15, y+15]
            self.canvas.create_oval(*dimensions, fill="#12f122")
            self.world.add_circle(x, y)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
