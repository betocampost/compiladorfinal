"""
Main file for the IDE
"""

import tkinter as tk
from tkinter import filedialog
from components.menu import MenuBar
from components.editor import Editor
from components.tabs import TabManager
from lexer import lexer
from parser_ import Parser


class IDE:
    """IDE main class"""

    def __init__(self, main):
        self.root = main
        self.root.title("IDE")
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

        # Create a main frame to hold the editor and the tabs
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.editor = Editor(self.main_frame)
        self.current_file = None

        self.tabs = TabManager(self.main_frame)

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
        self.tabs.lexycal_analysis_tab.clear_text()
        self.tabs.lexycal_analysis_errors_tab.clear_text()
        self.tabs.syntactic_analysis_tab.clear_tree()
        self.tabs.syntactic_analysis_errors_tab.clear_text()
        self.tabs.semantic_analysis_tab.clear_text()
        self.tabs.semantic_analysis_errors_tab.clear_text()
        self.tabs.hash_table_analysis_tab.clear_text()
        self.tabs.hash_table_errors_tab.clear_text()
        self.tabs.intermediate_code_analysis_tab.clear_text()
        self.tabs.intermediate_code_errors_tab.clear_text()
        self.tabs.results_tab.clear_text()

        if self.current_file:
            tokens, errors = lexer(self.current_file)

            token_str = "\n".join([str(token) for token in tokens])
            self.tabs.lexycal_analysis_tab.add_text(token_str)

            error_str = "\n".join([str(error) for error in errors])
            self.tabs.lexycal_analysis_errors_tab.add_text(error_str)

            if not errors:
                parser = Parser(tokens)
                raiz = parser.parse()
                self.tabs.syntactic_analysis_tab.set_tree(raiz)
        else:
            print("No file to run")


if __name__ == "__main__":
    root = tk.Tk()
    app = IDE(root)
    root.mainloop()
