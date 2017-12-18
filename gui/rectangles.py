import tkinter

# TOOLS
LINE, RECTANGLE = list(range(2))

class Paint:
    def __init__(self, canvas):
        self.canvas = canvas
        self._tool, self._obj = None, None
        self.lastx, self.lasty = None, None
        self.canvas.bind('<Button-1>', self.update_xy)
        self.canvas.bind('<B1-Motion>', self.draw)

    def draw(self, event):
        if self._tool is None or self._obj is None:
            return
        x, y = self.lastx, self.lasty
        if self._tool in (LINE, RECTANGLE):
            self.canvas.coords(self._obj, (x, y, event.x, event.y))

    def update_xy(self, event):
        if self._tool is None:
            return
        x, y = event.x, event.y
        if self._tool == LINE:
            self._obj = self.canvas.create_line((x, y, x, y))
        elif self._tool == RECTANGLE:
            self._obj = self.canvas.create_rectangle((x, y, x, y))
        self.lastx, self.lasty = x, y

    def select_tool(self, tool):
        print('Tool', tool)
        self._tool = tool

class Tool:
    def __init__(self, whiteboard, parent=None):
        self.whiteboard = whiteboard

        frame = tkinter.Frame(parent)
        self._curr_tool = None
        for i, (text, t) in enumerate((('L', LINE), ('R', RECTANGLE))):
            lbl = tkinter.Label(frame, text=text, width=2, relief='raised')
            lbl._tool = t
            lbl.bind('<Button-1>', self.update_tool)
            lbl.pack(padx=6, pady=6*(i % 2))
        frame.pack(side='left', fill='y', expand=True, pady=6)

    def update_tool(self, event):
        lbl = event.widget
        if self._curr_tool:
            self._curr_tool['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_tool = lbl
        self.whiteboard.select_tool(lbl._tool)


root = tkinter.Tk()

canvas = tkinter.Canvas(highlightbackground='black')
whiteboard = Paint(canvas)
tool = Tool(whiteboard)
canvas.pack(fill='both', expand=True, padx=6, pady=6)

root.mainloop()