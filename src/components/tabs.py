"""TabManager class to manage tabs in the notebook"""

import tkinter as tk
from tkinter import ttk


class TabManager:
    """TabManager class to manage tabs in the notebook"""

    def __init__(self, root):
        self.notebook = ttk.Notebook(root)
        self.notebook.place(relx=1, rely=0, relwidth=0.4, relheight=0.7, anchor=tk.NE)
        self.notebook_errors = ttk.Notebook(root)
        self.notebook_errors.place(
            relx=0, rely=1, relwidth=1, relheight=0.3, anchor=tk.SW
        )

        self.create_tabs()

    def create_tabs(self):
        """Create the tabs for the notebook"""

        self.lexycal_analysis_tab = Tab(self.notebook, "Lexico")
        self.syntactic_analysis_tab = TreeViewTab(self.notebook, "Sintactico")
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
    """TextTab class to manage tabs in the notebook"""

    def __init__(self, notebook, text):
        self.tab = ttk.Frame(notebook)
        self.text_widget = tk.Text(self.tab)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        notebook.add(self.tab, text=text)

    def add_text(self, text):
        """Add text to the tab"""
        self.text_widget.insert(tk.END, text)

    def clear_text(self):
        """Clear the text widget"""
        self.text_widget.delete(1.0, tk.END)


class TreeViewTab:
    """TreeViewTab class to manage tabs in the notebook"""

    def __init__(self, notebook, text):
        self.tab = ttk.Frame(notebook)
        self.tree = ttk.Treeview(self.tab)
        self.tree.pack(fill=tk.BOTH, expand=True)
        notebook.add(self.tab, text=text)

    def clear_tree(self):
        """Clear the tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def add_tree_node(self, parent, node):
        """Recursively add nodes to the tree view"""
        node_id = self.tree.insert(parent, "end", text=str(node))
        self.tree.item(node_id, open=True)  # This line expands the node
        for child in node.children:
            self.add_tree_node(node_id, child)

    def set_tree(self, root_node):
        """Set the tree view with the root node"""
        self.clear_tree()
        self.add_tree_node("", root_node)
