import sqlite3 as sq
from core.config import config

class SupportTicket:
    def __init__(self):
        self.db_path = config.path_db()
        self.connection = sq.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def check_thread(self, id_thread):
        info = self.cursor.execute(
            '''SELECT * FROM support_ticket WHERE id_thread=?''', (id_thread,))

        if info.fetchone() is None:
            return False
        else:
            return True

    def check_user(self, id_user):
        info = self.cursor.execute(
            '''SELECT * FROM support_ticket WHERE id_user=?''', (id_user,))

        if info.fetchone() is None:
            return False
        else:
            return True

    def id_user(self, id_thread):
        return self.cursor.execute(
            '''SELECT id_user FROM support_ticket WHERE id_thread=?''', (id_thread,)).fetchone()[0]

    def id_thread(self, id_user):
        return self.cursor.execute(
            '''SELECT id_thread FROM support_ticket WHERE id_user=?''', (id_user,)).fetchone()[0]

    def add_thread(self, id_thread, user_id):
        self.cursor.execute('''INSERT INTO support_ticket VALUES (?,?)''',
                            (id_thread, user_id))
        self.connection.commit()

    def delete_thread(self, id_user):

        self.cursor.execute('''DELETE FROM support_ticket WHERE id_user=?''', (id_user,))
        self.connection.commit()
