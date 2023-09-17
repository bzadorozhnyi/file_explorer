import os
import tkinter as tk

from navigation_panel import NavigationPanel
from path_listbox import PathListbox
from utils import get_parent_directory, open_file


class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("File Explorer")

        # Setup navigation panel
        self.nav_panel = NavigationPanel(
            master=self, open_parent_directory=self.open_parent_directory)
        self.nav_panel.pack(expand=True, fill='both', padx=5, pady=5)

        # Setup list box of files
        self.path_listbox = PathListbox(
            self, self._get_current_directory)
        self.path_listbox.pack()

        self.path_listbox.update_file_list()

        # BINDINGs
        self.nav_panel.search_bar.entry.bind(
            "<Return>", self.path_listbox.update_file_list)
        self.path_listbox.bind("<Double-1>", self.open_dir_or_file)

    def _get_current_directory(self) -> str:
        """Returns the directory that the user opened."""
        return self.nav_panel.search_bar.get_path()

    def open_dir_or_file(self, event=None):  # Event parameter required, but not used
        """Opens a file or directory depending on the path selected by the user."""
        # get selected path
        item = self.path_listbox.selection()[0]
        selected_path = self.path_listbox.item(item, "text")

        current_directory = self._get_current_directory()

        # in the search bar is file path, get parent directory of it
        if os.path.isfile(self._get_current_directory()):
            current_directory = get_parent_directory(current_directory)

        absolute_path = os.path.join(
            current_directory, selected_path)

        if os.path.isfile(absolute_path):
            open_file(absolute_path)
        elif os.path.isdir(absolute_path):
            self.__change_directory(absolute_path)

    def __change_directory(self, new_directory):
        """Changes the directory by user choice."""
        self.nav_panel.search_bar.path.set(new_directory)
        self.path_listbox.update_file_list()

    def open_parent_directory(self):
        """Opens the parent directory of the current directory."""
        parent_directory = get_parent_directory(self._get_current_directory())

        self.__change_directory(parent_directory)
