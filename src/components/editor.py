import tkinter as tk
from chlorophyll import CodeView
from pygments.lexer import RegexLexer, words
from pygments.token import (
    Text,
    Comment,
    Punctuation,
    Keyword,
    Operator,
    Number,
    Name,
    Error,
)
import toml


class CustomLexer(RegexLexer):
    tokens = {
        "root": [
            (r"\s+", Text),  # whitespace
            (r"//.*?\n", Comment.Singleline),  # single-line comments
            (
                r"/\*",
                Comment.Multiline,
                "comment",
            ),  # start of multiline comments
            (r"[(){};,]", Punctuation),  # symbols
            (
                words(
                    (
                        "if",
                        "else",
                        "do",
                        "while",
                        "switch",
                        "case",
                        "double",
                        "main",
                        "cin",
                        "cout",
                        "int",
                        "float",
                    ),
                    suffix=r"\b",
                ),
                Keyword,
            ),  # keywords
            (r"[+-/*%^]|\+\+|--|=|==|<=|>=|!=|<|>|and|or", Operator),  # operators
            (r"\b\d+(\.\d+)?\b", Number.Float),  # float numbers
            (r"\b\d+\b", Number.Integer),  # integers
            (r"[a-zA-Z_][a-zA-Z0-9_]*", Name.Variable),  # identifiers
            (r"[^\s]+", Error),  # error handling for invalid characters
        ],
        "comment": [
            (r"[^*/]+", Comment.Multiline),
            (r"/\*", Comment.Multiline, "#push"),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"[*/]", Comment.Multiline),
        ],
    }

    def get_tokens_unprocessed(self, text, stack=("root",)):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            print(f"Token: {token}, Value: {value}, Stack: {stack}")
            yield index, token, value


class Editor:
    """Editor for the IDE"""

    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.place(
            relx=0, rely=0, relwidth=0.6, relheight=0.7
        )  # Adjust the size and placement

        # Load custom color scheme from TOML file
        custom_color_scheme = toml.load("custom_color_scheme.toml")

        # Create CodeView with custom lexer and color scheme
        self.text_editor = CodeView(
            self.frame, lexer=CustomLexer(), color_scheme=custom_color_scheme
        )
        self.text_editor.pack(expand=1, fill="both")

        self.cursor_position_label = tk.Label(
            self.frame, text="Line: 1 Col: 1", anchor=tk.W
        )
        self.cursor_position_label.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)

        self.text_editor.bind("<ButtonRelease-1>", self.update_cursor_position)
        self.text_editor.bind("<KeyRelease>", self.update_cursor_position)

    def clear(self):
        """Clear the editor"""
        self.text_editor.delete(1.0, tk.END)

    def get_content(self):
        """Get the content of the editor"""
        return self.text_editor.get(1.0, tk.END)

    def set_content(self, content):
        """Set the content of the editor"""
        self.clear()
        self.text_editor.insert(tk.END, content)

    def update_cursor_position(self, event=None):
        """Update cursor position label"""
        cursor_position = self.text_editor.index(tk.INSERT)
        line, col = cursor_position.split(".")
        col = str(int(col) + 1)
        self.cursor_position_label.config(text=f"Line: {line} Col: {col}")


if __name__ == "__main__":
    root = tk.Tk()
    editor = Editor(root)
    root.mainloop()
