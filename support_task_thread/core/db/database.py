import sqlite3 as sq
from core.config import config


class DataBase:
    def __init__(self):
        self.db_path = config.path_db()
        self.connection = sq.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create(self):
        if self.connection:
            print(">> База подключена")
            self.__support_ticket()

    def __support_ticket(self):
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS support_ticket (
            id_thread INTEGER NOT NULL,
            id_user   INTEGER NOT NULL
            )''')
        self.connection.commit()
