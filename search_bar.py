import tkinter as tk
from tkinter import ttk


class SearchBar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.path = tk.StringVar()
        self.entry = ttk.Entry(textvariable=self.path)

        self.entry.pack(expand=True)

    def get_path(self):
        """Gets path printed in the search bar by the user."""
        return self.path.get()
