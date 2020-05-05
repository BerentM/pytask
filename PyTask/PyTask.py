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
        self.draw(self.master)

    def draw(self, master, destroy=0):
        """
        Draw whole contents of GUI.
        """
        last_row = 0
        self.db = dbh.dbHelper()
        tk.Label(master, text="Dodaj nowe zadanie.").grid(row=last_row,
                                                          columnspan=2,
                                                          sticky='NSEW')

        last_row += 1
        self.ent_task = tk.Entry(master, width=100)
        self.ent_task.grid(row=last_row, columnspan=2)

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
        table_labels = ('Numer zadania', 'Zadanie')
        for i, lbl in enumerate(table_labels):
            tk.Label(master, text=lbl, relief='ridge').grid(row=last_row,
                                                            column=i,
                                                            sticky='NSEW')

        task_list = self.db.get_tasks()
        if task_list:
            for i in range(len(task_list)):
                last_row += i
                for j in range(2):
                    lbl_table = tk.Label(master, text='%s' % (task_list[i][j]),
                                         relief='ridge')
                    lbl_table.grid(row=last_row, column=j, sticky='NSEW')

        self.master.focus_set()
        self.keybindings()

    def destroy_widgets(self):
        """
        Destroy widgets before recreating them in proper position
        """
        self.ent_task.destroy()
        self.btn_add.destroy()

    def add_task(self, event=None):
        """
        Add new task into database.
        """
        if self.ent_task.get():
            self.db.insert_task(self.ent_task.get())
            self.destroy_widgets()
            self.draw(self.master)

    def keybindings(self):
        """
        Set of keybindings used in PyTask.
        """
        self.master.bind_all("<Control-q>", lambda q: root.destroy())
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
frame = ScrollableFrame(root)
frame.pack()
pytask = PyTask(frame.scrollable_frame)

root.title("PyTask")
root.mainloop()
