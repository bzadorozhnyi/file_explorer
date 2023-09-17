import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from utils import open_file


class PathListbox(ttk.Treeview):
    def __init__(self, master=None, get_current_directory=lambda: ''):
        super().__init__(master, columns=[
            'Date modified', 'Size'], show='tree headings')

        # Setup component
        self.master = master
        self.get_current_directory = get_current_directory

        # Add headings
        self.heading('#0', text='Name')
        self.heading('Date modified', text='Date modified')
        self.heading('Size', text='Size')

        # Load images
        self._folder_image = tk.PhotoImage(file='./images/folder.png')
        self._file_image = tk.PhotoImage(file='./images/file.png')

        # Setup command menus
        self.__setup_command_menu()
        self.__setup_file_menu()

        # BINDINGs
        self.bind("<Button-3>", self.do_popup)
        self.bind("<F2>", self.rename)
        self.bind("<Delete>", self.delete_items)
        self.bind("<Escape>", self.unselect)

    def __setup_command_menu(self):
        self.create_menu = tk.Menu(self, tearoff=0)
        self.create_menu.add_command(label='File', command=self.create_file)
        self.create_menu.add_command(
            label='Folder', command=self.create_folder)

        self.command_menu = tk.Menu(self, tearoff=0)
        self.command_menu.add_cascade(label='Create', menu=self.create_menu)

    def __setup_file_menu(self):
        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label='Rename', command=self.rename)
        self.file_menu.add_command(label='Delete', command=self.delete_items)

    def insert(self, parent, index, *args, text, values, image):
        item_id = super().insert(parent, index, text=text, values=values, image=image)

        return item_id

    def unselect(self, event=None):
        if len(self.selection()) > 0:
            self.selection_remove(self.selection()[0])

    def delete_items(self, event=None):
        if self.selection() != ():
            for item in self.selection():
                selected_path = self.item(item, "text")

                absolute_path = os.path.join(
                    self.get_current_directory(), selected_path)

                if os.path.isfile(absolute_path):
                    os.remove(absolute_path)
                elif os.path.isdir(absolute_path):
                    os.rmdir(absolute_path)

            self.update_file_list()

    def rename(self, event=None):
        if self.selection() != ():
            item = self.selection()[0]
            selected_path = self.item(item, "text")

            window = tk.Toplevel(self)
            window.title("Rename")

            entry = ttk.Entry(window)
            entry.insert(0, selected_path)
            entry.pack()

            def handle_save(event=None):
                source = os.path.join(
                    self.get_current_directory(), selected_path)
                destionation = os.path.join(
                    self.get_current_directory(), entry.get())

                os.rename(source, destionation)

                self.update_file_list()
                window.destroy()

            save_button = ttk.Button(window, text='Save', command=handle_save)
            save_button.pack()

            entry.bind("<Return>", handle_save)

    def do_popup(self, event=None):
        def handle_popup(menu):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            except:
                menu.grab_release()

        if self.selection() == ():
            handle_popup(self.command_menu)
        else:
            handle_popup(self.file_menu)

    def create_save_form(self, window_title: str, placeholder: str, handle_save_callback: Callable[[str], None], event=None):
        """Creates a form to save file or folder."""
        window = tk.Toplevel(self)
        window.title(window_title)

        entry = ttk.Entry(window)
        entry.insert(0, placeholder)
        entry.pack()

        def handle_save(event=None):
            absolute_path = os.path.join(
                self.get_current_directory(), entry.get())
            handle_save_callback(absolute_path)
            self.update_file_list()

            window.destroy()

        save_button = ttk.Button(window, text='Save', command=handle_save)
        save_button.pack()

        entry.bind("<Return>", handle_save)

    def create_file(self, event=None):
        self.create_save_form("Create file", "New file",
                              lambda path: open(path, 'x'), event)

    def create_folder(self, event=None):
        self.create_save_form("Create folder", "New folder",
                              lambda path: os.mkdir(path), event)

    def update_file_list(self, event=None):  # Event parameter required, but not used
        """Updates current directory files list."""
        current_directory = self.get_current_directory()

        if os.path.isfile(current_directory):
            open_file(current_directory)
        elif os.path.isdir(current_directory):
            self.delete(*self.get_children())

            if current_directory != '':
                for path in os.listdir(current_directory):
                    absolute_path = os.path.join(current_directory, path)
                    if os.path.isdir(absolute_path):
                        self.insert("", "end", text=path, values=(self._get_modification_time(
                            path), self._get_file_size(path)), image=self._folder_image)
                    else:
                        self.insert("", "end", text=path, values=(
                            self._get_modification_time(path), self._get_file_size(path)), image=self._file_image)
        else:
            if current_directory != '':
                messagebox.showerror(
                    title="Not found", message="File or directory not found")

    def _get_file_size(self, path: str) -> str:
        """Returns file`s size in KB."""
        try:
            absolute_path = os.path.join(
                self.get_current_directory(), path)
            if os.path.isdir(absolute_path):
                return ""
            else:
                size = os.path.getsize(absolute_path) // 1000
                return f"{1 if size < 1 else size} KB"
        except FileNotFoundError:
            return ""

    def _get_modification_time(self, path: str) -> str:
        """Return file's modification time in format `dd:mm:yyyy HH:MM`."""
        try:
            absolute_path = os.path.join(
                self.get_current_directory(), path)
            modify_time = os.path.getmtime(absolute_path)
            return datetime.datetime.fromtimestamp(modify_time).strftime("%d.%m.%Y %H:%M")
        except FileNotFoundError:
            return ""
