# -*- coding: utf-8 -*-
__author__ = 'lundberg'


from contextlib import contextmanager
from neo4j.v1 import GraphDatabase, basic_auth


class Neo4jDBConnectionManager:

    """
    Every new connection is a transaction. To minimize new connection overhead for many reads we try to reuse a single
    connection. If this seem like a bad idea some kind of connection pool might work better.

    Neo4jDBConnectionManager.read()
    When using with Neo4jDBConnectionManager.read(): we will always rollback the transaction. All exceptions will be
    thrown.

    Neo4jDBConnectionManager.write()
    When using with Neo4jDBConnectionManager.write() we will always commit the transaction except when we see an
    exception. If we get an exception we will rollback the transaction and throw the exception.

    Neo4jDBConnectionManager.transaction()
    When we don't want to share a connection (transaction context) we can set up a new connection which will work
    just as the write context manager above but with it's own connection.
    """

    def __init__(self, dsn, username=None, password=None):
        self.dsn = dsn
        self.connection = connect(dsn, username, password)

    @contextmanager
    def _read(self):
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
            self.connection.rollback()
    read = property(_read)

    @contextmanager
    def _write(self):
        cursor = self.connection.cursor()
        try:
            yield cursor
        except self.connection.Error as e:
            cursor.close()
            self.connection.rollback()
            raise e
        else:
            cursor.close()
            self.connection.commit()
        finally:
            pass
    write = property(_write)

    @contextmanager
    def _transaction(self):
        connection = connect(self.dsn)
        cursor = connection.cursor()
        try:
            yield cursor
        except self.connection.Error as e:
            connection.rollback()
            raise e
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()
    transaction = property(_transaction)