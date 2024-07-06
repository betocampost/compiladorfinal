"""
Main file to run the application
"""

import tkinter as tk
from tkinter import filedialog
from components.menu import MenuBar
from components.editor import Editor


class IDE:
    """IDE main class"""

    def __init__(self, main):
        self.root = main
        self.root.title("My IDE")
        self.root.geometry("1024x768")

        self.menu_bar = MenuBar(
            self.root,
            new_file=self.new_file,
            open_file=self.open_file,
            save_file=self.save_file,
            save_as=self.save_as,
            open_folder=self.open_folder,
            run_code=self.run_code,
        )

        self.editor = Editor(self.root)  # Initialize the editor
        self.current_file = None

    def new_file(self):
        """Create a new file"""
        self.editor.clear()
        self.current_file = None  # Reset the current file

    def open_file(self):
        """Open a file dialog to open a file"""
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.editor.set_content(content)
            self.current_file = file_path  # Update the current file

    def save_file(self):
        """Save a file"""
        if self.current_file:
            # Save to the current file
            with open(self.current_file, "w", encoding="utf-8") as file:
                content = self.editor.get_content()
                file.write(content)
        else:
            # No current file, use save_as
            self.save_as()

    def save_as(self):
        """Save a file as"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                content = self.editor.get_content()
                file.write(content)
            self.current_file = file_path  # Update the current file

    def open_folder(self):
        """Open a folder"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            print(f"Opened folder: {folder_path}")

    def run_code(self):
        """Run the code"""
        print("Running code")


if __name__ == "__main__":
    root = tk.Tk()
    app = IDE(root)
    root.mainloop()
