# I'm trying to make a graph-like "database" editor
import tkinter as tk


class World():
    def __init__(self):
        self.circles = []

    def add_circle(self, x, y):
        self.circles += [{
            "position": (x, y),
            "connects_to": [],  # not a set() because these dicts are not hashable
        }]

    def find_circle(self, x, y):
        search_distance = 20
        for index, circle in enumerate(self.circles):
            if abs(circle['position'][0] - x) < search_distance and \
               abs(circle['position'][1] - y) < search_distance:
                return circle
        return None

    def connect_nodes(self, first, second):
        if second not in first["connects_to"]:
            first["connects_to"].append(second)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.world = World()

        self.update()
        width, height = self.master.winfo_width(), self.master.winfo_height()
        self.canvas = None
        self.create_widgets(width, height)
        self.bind_events()

        self.selected = None

    def create_widgets(self, width, height):
        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.canvas.pack()

    def bind_events(self):
        self.master.bind("<Button-1>", self.mouse_left_click)
        self.master.bind("<Button-3>", self.mouse_right_click)

    def draw_circle_shape(self, x, y, color):
        dimensions = [x-15, y-15, x+15, y+15]
        self.canvas.create_oval(*dimensions, fill=color)

    def mouse_left_click(self, event):
        x, y = event.x, event.y
        circle = self.world.find_circle(x, y)
        if circle:
            self.handle_click_on_circle(circle)
        else:
            self.create_new_circle(x, y)

    def mouse_right_click(self, event):
        if self.selected:
            x, y = self.selected['position'][0], self.selected['position'][1]
            self.draw_circle_shape(x, y, "#12f122")
            self.selected = None

    def create_new_circle(self, x, y):
        self.draw_circle_shape(x, y, "#12f122")
        self.world.add_circle(x, y)

    def handle_click_on_circle(self, clicked_circle):
        if not self.selected:
            self.select_circle(clicked_circle)
        else:
            self.connect_circles(self.selected, clicked_circle)

    def select_circle(self, circle):
        x, y = circle['position'][0], circle['position'][1]
        self.draw_circle_shape(x, y, "#42ffbd")
        self.selected = circle

    def connect_circles(self, first, second):
        self.world.connect_nodes(first, second)
        from_x, from_y= first['position'][0], first['position'][1]
        to_x, to_y = second['position'][0], second['position'][1]
        self.canvas.create_line(from_x, from_y, to_x, to_y, fill="#ff6f43")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
