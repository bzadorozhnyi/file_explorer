import tkinter as tk
from tkinter import ttk

from search_bar import SearchBar

class NavigationPanel(tk.Frame):
    def __init__(self, parent_dir_img, open_parent_directory, master=None):
        super().__init__(master=master)
        self.master = master

        self.parent_dir_button = ttk.Button(
            self, image=parent_dir_img, command=open_parent_directory)
        self.search_bar = SearchBar(self)

        self.search_bar.pack(side='left')
        self.parent_dir_button.pack(side='left')