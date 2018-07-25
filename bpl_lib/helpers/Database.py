import sqlite3

from bpl_lib.helpers.Constants import NETWORKS_DB

class Database:

    def __init__(self):
        """
        Creates database connection object. Used to interact with the Networks.db database
        """

        self._connection = sqlite3.connect(NETWORKS_DB)
        self._cursor = self._connection.cursor()

    def query(self, sql, parameters=()):
        """
        Querys Networks.db and returns result set

        :param sql: Valid SQLite statement
        :param parameters: Parameters to replace any placeholders in the statement
        :return: (list)
        """

        self._cursor.execute(sql, parameters)
        return self._cursor.fetchall()

    def _commit(self, sql, parameters):
        """
        Commit helper method. Executes a sql statement and commits the changes to Networks.db

        :param sql: Valid SQLite statement
        :param parameters: Parameters to replace any placeholders in the statement
        """

        self._cursor.execute(sql, parameters)
        self._connection.commit()

    def insert(self, sql, parameters=()):
        """
        Insert. Wrapper for self._commit

        :param sql: Valid SQLite statement
        :param parameters: Parameters to replace any placeholders in the statement
        """

        self._commit(sql, parameters)


    def delete(self, sql, parameters=()):
        """
        Delete. Wrapper for self._commit

        :param sql: Valid SQLite statement
        :param parameters: Parameters to replace any placeholders in the statement
        """

        self._commit(sql, parameters)


    def update(self, sql, parameters=()):
        """
        Update. Wrapper for self._commit

        :param sql: Valid SQLite statement
        :param parameters: Parameters to replace any placeholders in the statement
        """

        self._commit(sql, parameters)

    def close(self):
        """
        Closes the connection to Networks.db. Ensures any changes are commited.
        """

        self._connection.close()
