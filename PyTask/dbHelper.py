#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os


class dbHelper:
    """
    Helping class, designed to simplify working with sqlite database
    """
    def __init__(self):
        wdir = os.path.dirname(os.path.realpath(__file__))
        self.conn = sqlite3.connect(wdir + "/data/tasks.db")
        self.cur = self.conn.cursor()

    def init_database(self):
        """
        Create new database/tables if they don't exist.
        """
        self.cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER\
                         PRIMARY KEY, priority TEXT, date DATE, task TEXT,\
                         task_status INTEGER DEFAULT 0)")

    def purge_database(self):
        """
        Deletes all tables in database.
        """
        tables = self.cur.execute("SELECT name FROM sqlite_master WHERE\
                                  type='table'")
        for table_name in tables:
            self.cur.execute(f"DROP TABLE {table_name[0]}")

    def insert_task(self, priority, date, task_text):
        """
        Insert new task into database.
        ~~~~~~~~~~~~~~~~~~~~~~~~

        :task_text: short task description
        """
        self.cur.execute(f"INSERT INTO tasks(priority, date, task) VALUES\
                         ('{priority}', '{date}', '{task_text}')")
        self.conn.commit()

    def delete_task(self, task_id):
        self.cur.execute(f"DELETE FROM tasks WHERE id ={task_id}")
        self.conn.commit()

    def get_tasks(self):
        """
        Get list of tasks.
        """
        output = self.cur.execute("SELECT id, priority, date, task, task_status FROM tasks")
        if output:
            return output.fetchall()
        else:
            return []

    def get_selected_task(self, task_id):
        output = self.cur.execute(f"SELECT priority, date, task FROM tasks\
                                  WHERE id = {task_id}")
        if output:
            return output.fetchall()
        else:
            return []

    def update_task(self, task_id, priority=None, date=None, task_text=None, status=None):
        if priority:
            self.cur.execute(f"UPDATE tasks SET priority = '{priority}', date =\
                            '{date}', task = '{task_text}' WHERE id = {task_id}")
        elif status:
            self.cur.execute(f"UPDATE tasks SET task_status = CASE WHEN task_status = 0\
                             THEN 1 ELSE 0 END WHERE id = {task_id}")
        self.conn.commit()


if __name__ == "__main__":
    db = dbHelper()
    db.purge_database()
    db.init_database()
