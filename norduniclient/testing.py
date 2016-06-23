# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest
import time
import atexit
import random
import subprocess
from norduniclient.core import init_db
from norduniclient.exceptions import SocketError, OperationalError


__author__ = 'lundberg'


class Neo4jTemporaryInstance(object):
    """
    Singleton to manage a temporary Neo4j instance

    Use this for testing purpose only. The instance is automatically destroyed
    at the end of the program.

    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            atexit.register(cls._instance.shutdown)
        return cls._instance

    def __init__(self):
        self._port = random.randint(40000, 50000)
        self._docker_name = 'neo4j-{!s}'.format(self.port)
        self._process = subprocess.Popen(['docker', 'run', '--rm', '--name', '{!s}'.format(self._docker_name),
                                          '-p', '{!s}:7474'.format(self._port),
                                          'neo4j:2.1.8'],
                                         stdout=open('/tmp/neo4j-temp.log', 'wb'),
                                         stderr=subprocess.STDOUT)
        self._host = 'http://localhost'

        for i in range(10):
            time.sleep(0.2)
            try:
                self._db = init_db('{!s}:{!s}'.format(self._host, self._port))
            except (SocketError, OperationalError):
                continue
            else:
                break
        else:
            self.shutdown()
            assert False, 'Cannot connect to the neo4j test instance'

    @property
    def db(self):
        return self._db

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def purge_db(self):
        q = """
            MATCH (n:Node)
            OPTIONAL MATCH (n)-[r]-()
            DELETE n,r
            """
        with self.db.transaction as t:
            t.execute(q).fetchall()

    def shutdown(self):
        if self._process:
            # Due to the official neo4j container running the neo4j process with PID 1 the process can't be
            # stopped the usual way
            stop_proc = subprocess.Popen(['docker', 'stop', self._docker_name],
                                         stdout=open('/tmp/neo4j-temp.log', 'wb'),
                                         stderr=subprocess.STDOUT)
            print('Stopping neo4j docker container...')
            stop_proc.wait()
            print('Neo4j docker container stopped.')
            self._process.kill()
            self._process.wait()
            self._process = None


class Neo4jTestCase(unittest.TestCase):
    """
    Base test case that sets up a temporary Neo4j instance
    """

    neo4j_instance = Neo4jTemporaryInstance.get_instance()

    def setUp(self):
        self.neo4jdb = self.neo4j_instance.db

    def tearDown(self):
        self.neo4j_instance.purge_db()

    @classmethod
    def tearDownClass(cls):
        cls.neo4j_instance.shutdown()
