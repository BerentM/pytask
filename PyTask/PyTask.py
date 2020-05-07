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

__version__ = "0.1a"

import tkinter as tk
from tkinter import ttk
import PyTask.dbHelper as dbh


class PyTask:
    def __init__(self, master):
        self.master = master
        self.focused_widget = self.master.focus_get()
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
        self.ent_priority = tk.Entry(master, width=10)
        self.ent_priority.grid(row=last_row, column=0)
        self.ent_priority.insert(0, "B")

        self.ent_date = tk.Entry(master, width=10)
        self.ent_date.grid(row=last_row, column=1)
        self.ent_date.focus_get()

        self.ent_task = tk.Entry(master, width=100)
        self.ent_task.grid(row=last_row, column=2, columnspan=2)
        self.ent_task.focus_get()

        last_row += 1
        self.btn_add = tk.Button(master, text="Dodaj", command=self.add_task)
        self.btn_add.grid(row=last_row, column=0, sticky='NWSE')

        for i in range(1):
            last_row += 1
            tk.Label(master, text='').grid(row=last_row, column=0)

        last_row += 1
        tk.Label(master, text="Twoja lista zadań").grid(row=last_row,
                                                        columnspan=2,
                                                        sticky='NSEW')

        last_row += 1
        self.lbox_tasks = tk.Listbox(master)
        self.lbox_tasks.grid(row=last_row, columnspan=2, sticky='NSEW')

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
        Fill out task listbox.
        """
        self.lbox_tasks.delete(0, tk.END)
        ordered_col, asc = order_tuple
        task_list = self.db.get_tasks()
        task_list.sort(key=lambda tup: tup[ordered_col], reverse=asc)
        for task in task_list:
            self.lbox_tasks.insert(tk.END, task)

    def focus_widget(self, event):
        """
        Function switching focus between widgets.
        Currently unnecessary.
        """
        event.widget.tk_focusNext().focus()
        focused_widget = self.master.focus_get()
        self.modify_widget(focused_widget)

    def modify_widget(self, focused_widget):
        str_focused_widget = str(focused_widget)
        print(focused_widget)
        print(type(focused_widget))
        if str_focused_widget == '.!entry':
            print('entry')
            focused_widget.delete(0, 'end')
            focused_widget.insert(0, 'elo')

    def keybindings(self):
        """
        Set of keybindings used in PyTask.
        """
        self.master.bind_all("<Control-q>", lambda q: root.destroy())
        self.master.bind_all("<Control-m>", self.show_menu)
        self.master.bind_all("<Button-1>", lambda e: self.focus_widget(e))
        self.master.bind("<Tab>", self.focus_widget)
        # self.master.bind_all("<Control-1>", lambda c1: )
        # self.master.bind_all("<Control-2>", self.draw(self.master, 1, 0))
        self.master.bind("<a>", lambda a: self.ent_task.focus_set())
        self.ent_task.bind("<Return>", self.add_task)
        self.btn_add.bind("<Return>", self.add_task)


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
