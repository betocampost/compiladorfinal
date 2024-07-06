"""Editor"""

import tkinter as tk
from tkinter import scrolledtext


class Editor:
    """Editor for the IDE"""

    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.text_editor = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD)
        self.text_editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.line_number = LineNumber(self.frame, self.text_editor)
        self.line_number.pack(side=tk.LEFT, fill=tk.Y)

        self.text_editor.bind("<KeyRelease>", self.on_key_release)
        self.text_editor.bind("<ButtonRelease-1>", self.on_button_release)
        self.text_editor.bind("<Configure>", self.on_configure)

        self.text_editor.vbar.bind("<B1-Motion>", self.on_scroll)
        self.text_editor.vbar.bind("<ButtonRelease-1>", self.on_scroll)
        self.text_editor.bind("<MouseWheel>", self.on_scroll)

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

    def on_key_release(self, event):
        """Update line numbers on key release"""
        self.line_number.redraw()

    def on_button_release(self, event):
        """Update line numbers on button release"""
        self.line_number.redraw()

    def on_configure(self, event):
        """Update line numbers on configure event"""
        self.line_number.redraw()

    def on_scroll(self, event):
        """Update line numbers on scroll"""
        self.line_number.redraw()
        return "break"


class LineNumber(tk.Canvas):
    """Line number for the editor"""

    def __init__(self, root, text_widget):
        super().__init__(root, width=30, bg="lightgrey")
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self.redraw)
        self.text_widget.bind("<ButtonRelease-1>", self.redraw)
        self.text_widget.bind("<Configure>", self.redraw)

    def redraw(self, event=None):
        """Redraw the line numbers"""
        self.delete("all")
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            line_number = str(i).split(".", maxsplit=1)[0]
            self.create_text(2, y, anchor="nw", text=line_number)
            i = self.text_widget.index(f"{i}+1line")
