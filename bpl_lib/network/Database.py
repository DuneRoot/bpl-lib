import sqlite3

from bpl_lib.helpers.Constants import NETWORKS_DB_PATH

class Database:

    def __init__(self):
        self._connection = sqlite3.connect(NETWORKS_DB_PATH)
        self._cursor = self._connection.cursor()

    def query(self, sql, parameters=()):
        self._cursor.execute(sql, parameters)
        return self._cursor.fetchall()

    def _commit(self, sql, parameters):
        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def insert(self, sql, parameters=()):
        self._commit(sql, parameters)


    def delete(self, sql, parameters=()):
        self._commit(sql, parameters)


    def update(self, sql, parameters=()):
        self._commit(sql, parameters)

    def close(self):
        self._connection.close()
