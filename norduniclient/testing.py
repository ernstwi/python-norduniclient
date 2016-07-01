# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest
import time
import atexit
import random
import subprocess
import base64
import json
try:
    from http import client as http
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
    import httplib as http

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

    DEFAULT_USERNAME = 'neo4j'
    DEFAULT_PASSWORD = 'neo4j'
    TESTING_PASSWORD = 'testing'

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
                                          'docker.sunet.se/library/neo4j:2.2.8'],
                                         stdout=open('/tmp/neo4j-temp.log', 'wb'),
                                         stderr=subprocess.STDOUT)
        self._host = 'http://localhost'

        for i in range(100):
            time.sleep(0.2)
            try:
                self.change_password()
                self._db = init_db('{!s}:{!s}'.format(self._host, self._port), username='neo4j', password='testing')
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

    def change_password(self):
        """
        Changes the standard password from neo4j to testing to be able to run the test suite.
        """
        basic_auth = '%s:%s' % (self.DEFAULT_USERNAME, self.DEFAULT_PASSWORD)
        try:  # Python 2
            auth = base64.encodestring(basic_auth)
        except TypeError:  # Python 3
            auth = base64.encodestring(bytes(basic_auth, 'utf-8')).decode()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Basic %s" % auth.strip()
        }

        response = None
        retry = 0
        while not response:  # Retry if the server is not ready yet
            time.sleep(1)
            con = http.HTTPConnection('{!s}:{!s}'.format(self._host, self._port), timeout=10)
            try:
                con.request('GET', '{!s}:{!s}/user/neo4j'.format(self._host, self._port), headers=headers)
                response = json.loads(con.getresponse().read().decode('utf-8'))
            except ValueError:
                con.close()
            retry += 1
            if retry > 10:
                print("Could not change password for user neo4j")
                break
        if response and response.get('password_change_required', None):
            payload = json.dumps({'password': self.TESTING_PASSWORD})
            con.request('POST', '{!s}:{!s}/user/neo4j/password'.format(self._host, self._port), payload, headers)

        con.close()

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
    neo4jdb = neo4j_instance.db

    def tearDown(self):
        self.neo4j_instance.purge_db()

