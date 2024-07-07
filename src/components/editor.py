import tkinter as tk


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (
            args[0] in ("insert", "replace", "delete")
            or args[0:3] == ("mark", "set", "insert")
            or args[0:2] == ("xview", "moveto")
            or args[0:2] == ("xview", "scroll")
            or args[0:2] == ("yview", "moveto")
            or args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


class LineNumber(tk.Canvas):
    """Line number for the editor"""

    def __init__(self, root, text_widget):
        super().__init__(root, width=30, bg="lightgrey")
        self.text_widget = text_widget

    def attach(self, text_widget):
        self.text_widget = text_widget

    def redraw(self, *args):
        """Redraw the line numbers"""
        self.delete("all")

        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".", maxsplit=1)[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.text_widget.index(f"{i}+1line")


class Editor:
    """Editor for the IDE"""

    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.place(
            relx=0, rely=0, relwidth=0.6, relheight=0.7
        )  # Adjust the size and placement

        self.text_editor = CustomText(self.frame, wrap=tk.WORD)
        self.vsb = tk.Scrollbar(
            self.frame, orient="vertical", command=self.text_editor.yview
        )
        self.text_editor.configure(yscrollcommand=self.vsb.set)
        self.line_number = LineNumber(self.frame, self.text_editor)
        self.line_number.attach(self.text_editor)

        self.vsb.place(relx=0.95, rely=0, relheight=0.95)
        self.line_number.place(relx=0, rely=0, relheight=0.95)
        self.text_editor.place(relx=0.05, rely=0, relwidth=0.9, relheight=0.95)

        self.text_editor.bind("<<Change>>", self.on_change)
        self.text_editor.bind("<Configure>", self.on_change)

        self.cursor_position_label = tk.Label(
            self.frame, text="Line: 1 Col: 1", anchor=tk.W
        )
        self.cursor_position_label.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

        self.text_editor.bind("<Configure>", self.on_change)
        self.text_editor.bind("<ButtonRelease-1>", self.update_cursor_position)
        self.text_editor.bind("<KeyRelease>", self.update_cursor_position)

    def clear(self):
        """Clear the editor"""
        self.text_editor.delete(1.0, tk.END)
        self.line_number.redraw()

    def get_content(self):
        """Get the content of the editor"""
        return self.text_editor.get(1.0, tk.END)

    def set_content(self, content):
        """Set the content of the editor"""
        self.clear()
        self.text_editor.insert(tk.END, content)
        self.line_number.redraw()

    def on_change(self, event):
        """Update line numbers on change"""
        self.line_number.redraw()

    def update_cursor_position(self, event=None):
        """Update cursor position label"""
        cursor_position = self.text_editor.index(tk.INSERT)
        line, col = cursor_position.split(".")
        col = str(int(col) + 1)
        self.cursor_position_label.config(text=f"Line: {line} Col: {col}")
