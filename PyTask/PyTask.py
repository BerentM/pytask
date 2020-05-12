#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyTask is a todo.txt GUI, written in Python.
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2020 by Mateusz Berent.
:license: Apache 2.0, see LICENSE for more details.
:author: Mateusz Berent
:maintainer: Mateusz Berent
:email: berentm@protonmail.com
"""

__version__ = "0.2a"

import tkinter as tk
from tkinter import ttk
import PyTask.dbHelper as dbh
from datetime import datetime


class PyTask:
    def __init__(self, master):
        self.master = master
        self.focused_widget = self.master.focus_get()
        self.default_values()
        self.draw(self.master)

    def root_config(self, root):
        """
        Konfiguracja głównego okna.
        """
        root.title("PyTask")

    def show_menu(self, event):
        """
        Menu configuration.
        """
        self.menubar = tk.Menu(self.master)
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.do_nothing)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.post(event.x_root, event.y_root)

    def do_nothing(self, event):
        """
        Dummy function.
        """
        filewin = tk.Toplevel(self.master)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()

    def draw(self, master):
        """
        Draw contents of GUI.
        """
        last_row = 0
        self.db = dbh.dbHelper()
        tk.Label(master, text="Dodaj nowe zadanie.").grid(row=last_row,
                                                          columnspan=2,
                                                          sticky='NSEW')

        last_row += 1
        self.ent_priority = tk.Entry(master, width=10, fg='gray')
        self.ent_priority.grid(row=last_row, column=0)
        self.ent_priority.insert(0, self.priority)

        self.ent_date = tk.Entry(master, width=10)
        self.ent_date.grid(row=last_row, column=1)
        self.ent_date.insert(0, self.today)

        self.ent_task = tk.Entry(master, width=100)
        self.ent_task.grid(row=last_row, column=2, columnspan=2)

        last_row += 1
        self.btn_add = tk.Button(master, text="Dodaj", command=self.add_task)
        self.btn_add.grid(row=last_row, column=0, sticky='NWSE')

        last_row += 1
        tk.Label(master, text='').grid(row=last_row, column=0)

        last_row += 1
        tk.Label(master, text="Lista zadań").grid(row=last_row, columnspan=2,
                                                  sticky='NSEW')

        last_row += 1
        self.lbox_tasks = tk.Listbox(master)
        self.lbox_tasks.grid(row=last_row, columnspan=4, sticky='NSEW')
        # self.selection = 0
        # self.lbox_tasks.select_set(self.selection)

        last_row += 1
        self.btn_add = tk.Button(master, text="Zmień", command=self.add_task)
        self.btn_add.grid(row=last_row, column=0, sticky='NWSE')

        self.btn_add = tk.Button(master, text="Usuń", command=self.add_task)
        self.btn_add.grid(row=last_row, column=1, sticky='NWSE')

        # TODO ustawic cos co bedzie zwracalo krotke z 2 parametrami
        order_tuple = (0, 0)
        self.fill_task_listbox(order_tuple)
        self.master.focus_set()
        self.keybindings()

    def destroy_widgets(self):
        """
        Destroy widgets before recreating them in proper position.
        """
        self.ent_task.destroy()
        # self.btn_add.destroy()
        self.lbox_tasks.destroy()

    def add_task(self, event=None):
        """
        Add new task into database.
        """
        if self.ent_task.get():
            self.db.insert_task(self.ent_task.get())
            self.destroy_widgets()
            self.draw(self.master)
            self.master.focus_set()

    def fill_task_listbox(self, order_tuple):
        """
        Fill out task list box.
        """
        self.lbox_tasks.delete(0, tk.END)
        ordered_col, asc = order_tuple
        task_list = self.db.get_tasks()
        task_list.sort(key=lambda tup: tup[ordered_col], reverse=asc)
        for task in task_list:
            self.lbox_tasks.insert(tk.END, task)

    def focus_widget(self, event, mouse=0, fnext=1):
        """
        Function switching focus between widgets.
        ~~~~~~~~~
        :mouse: param used to check if mouse was used to focus current widget
        :fnext: param used to recognize keybinding Shift-Tab
        """
        if not mouse:
            if fnext:
                event.widget.tk_focusNext().focus()
            else:
                event.widget.tk_focusPrev().focus()
        focused_widget = self.master.focus_get()
        # print(focused_widget)
        self.modify_focused_widget(focused_widget)

    def modify_focused_widget(self, focused_widget):
        """
        Modifying currently focused widget.
        """
        if str(self.prev_entry) == '.!entry':
            if not self.prev_entry.get():
                self.prev_entry.insert(0, self.priority)
        elif str(self.prev_entry) == '.!entry2':
            if not self.prev_entry.get():
                self.prev_entry.insert(0, self.today)

        str_focused_widget = str(focused_widget)
        if str_focused_widget == '.!entry':
            focused_widget.delete(0, 'end')
            self.prev_entry = focused_widget
        elif str_focused_widget == '.!entry2':
            focused_widget.delete(0, 'end')
            self.prev_entry = focused_widget
        elif str_focused_widget == '.!entry3':
            self.prev_entry = focused_widget
            pass
        elif str_focused_widget == '.!listbox':
            # keyboard support is based on function entry_selection
            # mouse support
            # self.lbox_selected = self.lbox_tasks.get(tk.ANCHOR)
            # print(self.lbox_selected)
            pass

    def keybindings(self):
        """
        Set of keybindings used in PyTask.
        """
        self.master.bind_all("<Control-q>", lambda q: root.destroy())
        self.master.bind_all("<Control-m>", self.show_menu)
        self.master.bind("<Button-1>", lambda x: self.focus_widget(x, 1))
        self.master.bind("<Tab>", lambda x: self.focus_widget(x))
        self.master.bind("<Shift-ISO_Left_Tab>",
                         lambda x: self.focus_widget(x, 0, 0))
        self.master.bind("<a>", lambda a: self.ent_task.focus_set())
        self.ent_task.bind("<Return>", self.add_task)
        self.btn_add.bind("<Return>", self.add_task)
        self.lbox_tasks.bind("<<ListboxSelect>>", self.entry_selection)

    def default_values(self):
        """
        Init default variables.
        """
        self.priority = "B"
        self.today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        self.prev_entry = None

    def entry_selection(self, event):
        """
        Listbox selection logic.
        """
        if self.lbox_tasks.curselection():
            self.selection = self.lbox_tasks.curselection()[0]
        else:
            self.selection = 0
        self.lbox_tasks.select_set(self.selection)
        self.lbox_selected = self.lbox_tasks.selection_get()
        print(self.selection)
        print(self.lbox_selected)


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=600, width=800)
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        self.scrollable_frame.focus_set()

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)


root = tk.Tk()
# frame = ScrollableFrame(root)
# frame.pack()
# pytask = PyTask(frame.scrollable_frame)
pytask = PyTask(root)

pytask.root_config(root)
root.mainloop()
