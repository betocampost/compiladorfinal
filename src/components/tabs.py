import tkinter as tk
from tkinter import ttk, Text


class TabManager:
    """TabManager class to manage tabs in the notebook"""

    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.place(relx=1, rely=0, relwidth=0.4, relheight=1, anchor=tk.NE)
        self.notebook_errors = ttk.Notebook(root)
        self.notebook_errors.place(
            relx=0, rely=1, relwidth=1, relheight=0.3, anchor=tk.SW
        )

        self.create_tabs()

    def create_tabs(self):
        """Create the tabs for the notebook"""

        self.lexycal_analysis_tab = Tab(self.notebook, "Lexico")
        self.syntactic_analysis_tab = TreeView_Tab(self.notebook, "Sintactico")
        self.semantic_analysis_tab = Tab(self.notebook, "Semantico")
        self.hash_table_analysis_tab = Tab(self.notebook, "Hash Table")
        self.intermediate_code_analysis_tab = Tab(self.notebook, "Codigo Intermedio")
        self.results_tab = Tab(self.notebook, "Resultados")

        self.lexycal_analysis_errors_tab = Tab(self.notebook_errors, "Errores Lexicos")
        self.syntactic_analysis_errors_tab = Tab(
            self.notebook_errors, "Errores Sintacticos"
        )
        self.semantic_analysis_errors_tab = Tab(
            self.notebook_errors, "Errores Semanticos"
        )
        self.hash_table_errors_tab = Tab(self.notebook_errors, "Errores Hash Table")
        self.intermediate_code_errors_tab = Tab(
            self.notebook_errors, "Errores Codigo Intermedio"
        )


class Tab:
    """Tab class to manage tabs in the notebook"""

    def __init__(self, notebook, text):
        self.tab = tk.Frame(notebook)
        self.content = Text(self.tab, wrap=tk.WORD)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.content.config(state=tk.DISABLED)
        notebook.add(self.tab, text=text)

    def add_text(self, text):
        """Add text to the tab"""
        self.content.config(state=tk.NORMAL)
        self.content.delete(1.0, tk.END)
        self.content.insert(1.0, text)
        self.content.config(state=tk.DISABLED)


class TreeView_Tab:
    """TreeView_Tab class to manage tabs in the notebook"""

    def __init__(self, notebook, text):
        self.tab = tk.Frame(notebook)
        self.tree = ttk.Treeview(self.tab)
        self.tree.pack(fill=tk.BOTH, expand=True)
        notebook.add(self.tab, text=text)

    def add_tree(self):
        """Add tree to the tab"""
