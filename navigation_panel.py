import tkinter as tk
from tkinter import ttk

from search_bar import SearchBar


class NavigationPanel(tk.Frame):
    def __init__(self, open_parent_directory, master=None):
        super().__init__(master=master)
        self.master = master

        # Load image
        self._up_arrow = tk.PhotoImage(file='./images/up-arrow.png')

        self.parent_dir_button = ttk.Button(
            self, image=self._up_arrow, command=open_parent_directory)
        self.search_bar = SearchBar(self)

        self.parent_dir_button.pack(side='left')
        self.search_bar.pack(side='left', fill='x', expand=True)
