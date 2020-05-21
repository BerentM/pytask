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

__version__ = "0.3a"

import re
import tkinter as tk
from datetime import datetime
import PyTask.dbHelper as dbh


class PyTask:
    def __init__(self, master):
        self.master = master
        self.db = dbh.dbHelper()
        self.focused_widget = self.master.focus_get()
        self.default_values()
        self.draw(self.master)

    def root_config(self, root):
        """
        Main window configuration.
        """
        root.title("PyTask")
        root.geometry("850x600")

    def default_values(self):
        """
        Init default variables.
        """
        self.priority = "B"
        self.today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        self.prev_entry = None

    def draw(self, master):
        """
        Draw contents of GUI.
        """
        last_row = 0
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
        tk.Label(master, text=" Lista zadań").grid(row=last_row, columnspan=2,
                                                   sticky='NSW')

        last_row += 1
        self.lbox_tasks = tk.Listbox(master, selectmode='Single', height=20)
        self.lbox_tasks.grid(row=last_row, columnspan=4, sticky='NSEW')

        last_row += 1
        self.btn_change = tk.Button(master, text="Zmień",
                                    command=self.modify_task)
        self.btn_change.grid(row=last_row, column=0, sticky='NWSE')

        self.btn_delete = tk.Button(master, text="Usuń",
                                    command=self.delete_task)
        self.btn_delete.grid(row=last_row, column=1, sticky='NWSE')

        self.btn_switch = tk.Button(master, text="Status",
                                    command=self.switch_status)
        self.btn_switch.grid(row=last_row, column=2, sticky='NWS')

        order_tuple = (0, 0)
        self.fill_task_listbox(order_tuple)
        self.keybindings()

    def destroy_widgets(self):
        """
        Destroy widgets before recreating them in proper position.
        """
        self.ent_task.destroy()
        self.lbox_tasks.destroy()

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

    def listbox_selection(self, event):
        """
        Listbox selection logic.
        """
        if self.lbox_tasks.curselection():
            self.selection = self.lbox_tasks.curselection()[0]
            self.lbox_selected = self.lbox_tasks.selection_get()
            self.selected_task_id = re.search(r'\d*',
                                              self.lbox_selected).group()

    def format_task(self, task=[1, 'xyz']):
        task_id, priority, date, task, task_status = task
        if task_status == 1:
            task_status = '✓'
        else:
            task_status = '_'
        return "{:<3}|{:^3}|{:^12}| {: <50}|{:>5}".format(task_id, priority,
                                                          date, task,
                                                          task_status)

    def fill_task_listbox(self, order_tuple):
        """
        Fill out task list box.
        """
        self.lbox_tasks.delete(0, tk.END)
        ordered_col, asc = order_tuple
        task_list = self.db.get_tasks()
        task_list.sort(key=lambda tup: tup[ordered_col], reverse=asc)
        for task in task_list:
            self.lbox_tasks.insert(tk.END, self.format_task(task))

    def add_task(self, event=None):
        """
        Add new task into database.
        """
        if self.ent_task.get():
            self.db.insert_task(self.ent_priority.get(), self.ent_date.get(),
                                self.ent_task.get())
            self.draw(self.master)
            self.lbox_tasks.focus_set()
            self.lbox_tasks.activate(self.lbox_tasks.size()-1)
            self.lbox_tasks.selection_set(self.lbox_tasks.size()-1)
            self.lbox_tasks.see(self.lbox_tasks.size()-1)

    def delete_task(self, event=None):
        """
        Remove task from database.
        """
        self.db.delete_task(self.selected_task_id)
        self.lbox_tasks.delete(self.selection)

    def modify_task(self, event=None):
        """
        Modify selected task.
        """
        def modify_database(mod_window, priority, date, task_text):
            self.db.update_task(self.selected_task_id, priority, date,
                                task_text)
            self.draw(self.master)
            mod_window.destroy()

        try:
            db_output = self.db.get_selected_task(self.selected_task_id)[0]

            mod_window = tk.Toplevel(self.master)
            lbl_priority = tk.Label(mod_window, text="Priorytet: ")
            lbl_priority.grid(row=0, column=0, sticky="NSW")
            ent_priority = tk.Entry(mod_window)
            ent_priority.grid(row=0, column=1)
            ent_priority.insert(0, db_output[0])

            lbl_date = tk.Label(mod_window, text="Data: ")
            lbl_date.grid(row=1, column=0, sticky="NSWE")
            ent_date = tk.Entry(mod_window)
            ent_date.grid(row=1, column=1, sticky="NSWE")
            ent_date.insert(0, db_output[1])

            lbl_task = tk.Label(mod_window, text="Zadanie: ")
            lbl_task.grid(row=2, column=0, sticky="NSWE")
            ent_task = tk.Entry(mod_window)
            ent_task.grid(row=2, column=1, sticky="NSWE")
            ent_task.insert(0, db_output[2])

            btn_cancel = tk.Button(mod_window, text="Anuluj")
            btn_cancel.grid(row=3, column=0, sticky="NSWE")
            btn_ok = tk.Button(mod_window, text="Ok", command=lambda:
                               modify_database(mod_window, ent_priority.get(),
                                               ent_date.get(), ent_task.get()))
            btn_ok.grid(row=3, column=1, sticky="NSWE")
        except Exception:
            pass

    def switch_status(self):
        self.db.update_task(self.selected_task_id, status=1)
        order_tuple = (0, 0)
        self.fill_task_listbox(order_tuple)

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
        self.btn_delete.bind("<Return>", self.delete_task)
        self.lbox_tasks.bind("<d>", self.delete_task)
        self.lbox_tasks.bind("<Delete>", self.delete_task)
        self.lbox_tasks.bind("<<ListboxSelect>>", self.listbox_selection)
        self.lbox_tasks.bind("<Return>", self.modify_task)


root = tk.Tk()
pytask = PyTask(root)

pytask.root_config(root)
root.mainloop()
