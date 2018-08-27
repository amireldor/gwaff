# I'm trying to make a graph-like "database" editor
import tkinter as tk
from collections import namedtuple


Position = namedtuple("Position", ["x", "y"])


class World():
    def __init__(self):
        self.nodes = []

    def add_node(self, x, y):
        self.nodes += [{
            "position": Position(x, y),
            # Next Line: not a set() because these dicts are not hashable
            "connects_to": [],
        }]

    def find_node(self, x, y):
        search_distance = 20
        for index, node in enumerate(self.nodes):
            if abs(node['position'].x - x) < search_distance and \
               abs(node['position'].y - y) < search_distance:
                return node
        return None

    def connect_nodes(self, first, second):
        if second not in first["connects_to"]:
            first["connects_to"].append(second)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.world = World()
        self.master.geometry("800x660")
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

    def draw_node_shape(self, x, y, color):
        dimensions = [x-15, y-15, x+15, y+15]
        self.canvas.create_oval(*dimensions, fill=color)

    def mouse_left_click(self, event):
        x, y = event.x, event.y
        node = self.world.find_node(x, y)
        if node:
            self.handle_click_on_node(node)
        else:
            self.create_new_node(x, y)

    def mouse_right_click(self, event):
        if self.selected:
            x, y = self.selected['position'].x, self.selected['position'].y
            self.draw_node_shape(x, y, "#12f122")
            self.selected = None

    def create_new_node(self, x, y):
        self.draw_node_shape(x, y, "#12f122")
        self.world.add_node(x, y)

    def handle_click_on_node(self, clicked_node):
        if not self.selected:
            self.select_node(clicked_node)
        else:
            self.connect_nodes(self.selected, clicked_node)

    def select_node(self, node):
        x, y = node['position'].x, node['position'].y
        self.draw_node_shape(x, y, "#42ffbd")
        self.selected = node

    def connect_nodes(self, first, second):
        self.world.connect_nodes(first, second)
        from_x, from_y = first['position'].x, first['position'].y
        to_x, to_y = second['position'].x, second['position'].y
        self.canvas.create_line(from_x, from_y, to_x, to_y, fill="#ff6f43")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
