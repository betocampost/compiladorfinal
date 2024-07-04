"""
Menu for the application with File, Edit, and Run options.
"""

from io import BytesIO
import tkinter as tk
from tkinter import Menu, Menubutton
from PIL import Image, ImageTk
import cairosvg


class MenuBar:
    """Menu bar for the application"""

    def __init__(
        self, root, new_file, open_file, save_file, save_as, open_folder, run_code
    ):
        self.root = root
        self.menu_bar = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        self.menu_bar.pack(side=tk.TOP, fill=tk.X)
        self.create_menus(new_file, open_file, save_file, save_as, open_folder)
        self.configure_icons(
            new_file, open_file, save_file, save_as, open_folder, run_code
        )

    def create_menus(self, new_file, open_file, save_file, save_as, open_folder):
        """Create the File, Edit, and Run menus with options"""

        # Create a File menu
        file_menubutton = Menubutton(self.menu_bar, text="File", relief=tk.RAISED)
        file_menu = Menu(file_menubutton, tearoff=0)
        file_menu.add_command(label="New File", command=new_file)
        file_menu.add_command(label="Open File", command=open_file)
        file_menu.add_command(label="Save", command=save_file)
        file_menu.add_command(label="Save As", command=save_as)
        file_menu.add_command(label="Open Folder", command=open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        file_menubutton.config(menu=file_menu)
        file_menubutton.pack(side=tk.LEFT, padx=2, pady=2)

        # Create an Edit menu
        edit_menubutton = Menubutton(self.menu_bar, text="Edit", relief=tk.RAISED)
        edit_menu = Menu(edit_menubutton, tearoff=0)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        edit_menubutton.config(menu=edit_menu)
        edit_menubutton.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a Run menu
        run_menubutton = Menubutton(self.menu_bar, text="Run", relief=tk.RAISED)
        run_menu = Menu(run_menubutton, tearoff=0)
        run_menu.add_command(label="Compile")
        run_menubutton.config(menu=run_menu)
        run_menubutton.pack(side=tk.LEFT, padx=2, pady=2)

    def configure_icons(
        self, new_file, open_file, save_file, save_as, open_folder, run_code
    ):
        """Configure icons for the menu"""
        # Resize images for buttons
        self.new_icon = self.resize_svg("src/icons/add_file.svg", 24, 24)
        self.open_icon = self.resize_svg("src/icons/open_file.svg", 24, 24)
        self.save_icon = self.resize_svg("src/icons/save_file.svg", 24, 24)
        self.save_as_icon = self.resize_svg("src/icons/save_as.svg", 24, 24)
        self.folder_icon = self.resize_svg("src/icons/open_folder.svg", 24, 24)
        self.run_icon = self.resize_svg("src/icons/run.svg", 24, 24)

        # Add buttons to the custom menu bar with resized icons
        new_button = tk.Button(
            self.menu_bar,
            image=self.new_icon,
            command=new_file,
            width=30,
            height=30,
        )
        new_button.pack(side=tk.LEFT, padx=2, pady=2)

        open_button = tk.Button(
            self.menu_bar,
            image=self.open_icon,
            command=open_file,
            width=30,
            height=30,
        )
        open_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_button = tk.Button(
            self.menu_bar,
            image=self.save_icon,
            command=save_file,
            width=30,
            height=30,
        )
        save_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_as_button = tk.Button(
            self.menu_bar,
            image=self.save_as_icon,
            command=save_as,
            width=30,
            height=30,
        )
        save_as_button.pack(side=tk.LEFT, padx=2, pady=2)

        folder_button = tk.Button(
            self.menu_bar,
            image=self.folder_icon,
            command=open_folder,
            width=30,
            height=30,
        )
        folder_button.pack(side=tk.LEFT, padx=2, pady=2)

        run_button = tk.Button(
            self.menu_bar,
            image=self.run_icon,
            command=run_code,
            width=30,
            height=30,
        )
        run_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Add the menu bar to the root window
        self.root.config(menu=self.menu_bar)

    def resize_svg(self, file_path, width, height):
        """Resize an SVG image to the specified width and height"""
        png_data = cairosvg.svg2png(url=file_path)
        image = Image.open(BytesIO(png_data))
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
