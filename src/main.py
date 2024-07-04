"""
Main file to run the application
"""

import tkinter as tk
from tkinter import filedialog
from components.menu import MenuBar  # Import your new MenuBar class


class MyIDE:
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

    def new_file(self):
        """Create a new file"""
        print("New file")

    def open_file(self):
        """Open a file dialog to open a file"""
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"Opened file: {file_path}")

    def save_file(self):
        """Save a file"""
        print("Saving file")

    def save_as(self):
        """Save a file as"""
        print("Saving file as")

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
    app = MyIDE(root)
    root.mainloop()
