# -*- coding: utf-8 -*-

from __future__ import absolute_import

from norduniclient.core import init_db

__author__ = 'lundberg'


# Init as singleton for easy use in Django
neo4jdb = init_db()

