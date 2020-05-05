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
                         PRIMARY KEY, task TEXT)")

    def purge_database(self):
        """
        Deletes all tables in database.
        """
        tables = self.cur.execute("SELECT name FROM sqlite_master WHERE\
                                  type='table'")
        for table_name in tables:
            self.cur.execute(f"DROP TABLE {table_name[0]}")

    def insert_task(self, task_text):
        """
        Insert new task into database.
        ~~~~~~~~~~~~~~~~~~~~~~~~

        :task_text: short task description
        """
        self.cur.execute(f"INSERT INTO tasks(task) VALUES ('{task_text}')")
        self.conn.commit()

    def get_tasks(self):
        """
        Get list of tasks.
        """
        output = self.cur.execute("SELECT id, task FROM tasks")
        if output:
            return output.fetchall()
        else:
            return []


if __name__ == "__main__":
    db = dbHelper()
    db.purge_database()
    db.init_database()
