# -*- coding: utf-8 -*-

from __future__ import absolute_import

from norduniclient.testing import Neo4jTestCase
from norduniclient import core
from norduniclient import exceptions

__author__ = 'lundberg'


class CoreTests(Neo4jTestCase):

    def setUp(self):
        super(CoreTests, self).setUp()
        core.create_node(self.neo4jdb, name='Test Node 1', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='1')
        core.create_node(self.neo4jdb, name='Test Node 2', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='2')

    def test_create_and_get_node(self):
        core.create_node(self.neo4jdb, name='Test Node 3', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='3')
        node = core.get_node(self.neo4jdb, handle_id='3')
        self.assertIsInstance(node, dict)
        self.assertEqual(node.get('handle_id'), '3')

    def test_create_node_existing_node_handle(self):
        self.assertRaises(exceptions.IntegrityError, core.create_node, self.neo4jdb, name='Test Node 1',
                          meta_type_label='Logical', type_label='Test_Node', handle_id='1')

    def test_get_node_bundle(self):
        node_bundle = core.get_node_bundle(self.neo4jdb, handle_id='1')
        self.assertIsInstance(node_bundle, dict)
        node_data = node_bundle.get('data')
        self.assertIsInstance(node_data, dict)
        self.assertEqual(node_data.get('handle_id'), '1')
        self.assertEqual(node_bundle.get('meta_type'), 'Logical')
        self.assertIsInstance(node_bundle.get('labels'), list)
        self.assertIn('Test_Node', node_bundle.get('labels'))

    def test_delete_node(self):
        core.delete_node(self.neo4jdb, handle_id='1')
        self.assertRaises(exceptions.NodeNotFound, core.get_node, self.neo4jdb, handle_id='1')

    def test_create_relationship(self):
        relationship_id = core._create_relationship(self.neo4jdb, handle_id='1', other_handle_id='2', rel_type='Tests')
        self.assertIsInstance(relationship_id, int)

    def test_create_location_relationship(self):
        core.create_node(self.neo4jdb, name='Location Node 1', meta_type_label='Location',
                         type_label='Test_Node', handle_id='3')
        core.create_node(self.neo4jdb, name='Location Node 2', meta_type_label='Location',
                         type_label='Test_Node', handle_id='4')
        relationship_id = core.create_location_relationship(self.neo4jdb, location_handle_id='3', other_handle_id='4',
                                                            rel_type='Has')
        self.assertIsInstance(relationship_id, int)

    def test_failing_create_location_relationship(self):
        core.create_node(self.neo4jdb, name='Location Node 1', meta_type_label='Location',
                         type_label='Test_Node', handle_id='3')
        core.create_node(self.neo4jdb, name='Logical Node 2', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='4')
        self.assertRaises(exceptions.NoRelationshipPossible, core.create_location_relationship, self.neo4jdb,
                          location_handle_id='3', other_handle_id='4', rel_type='Has')

    def test_create_logical_relationship(self):
        core.create_node(self.neo4jdb, name='Logical Node 1', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='3')
        core.create_node(self.neo4jdb, name='Physical Node 2', meta_type_label='Physical',
                         type_label='Test_Node', handle_id='4')
        core.create_node(self.neo4jdb, name='Logical Node 2', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='5')

        relationship_id = core.create_logical_relationship(self.neo4jdb, logical_handle_id='3', other_handle_id='4',
                                                           rel_type='Depends_on')
        self.assertIsInstance(relationship_id, int)

        relationship_id = core.create_logical_relationship(self.neo4jdb, logical_handle_id='3', other_handle_id='5',
                                                           rel_type='Depends_on')
        self.assertIsInstance(relationship_id, int)

        relationship_id = core.create_logical_relationship(self.neo4jdb, logical_handle_id='3', other_handle_id='4',
                                                           rel_type='Part_of')
        self.assertIsInstance(relationship_id, int)

    def test_failing_create_logical_relationship(self):
        core.create_node(self.neo4jdb, name='Logical Node 1', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='3')
        core.create_node(self.neo4jdb, name='Physical Node 2', meta_type_label='Physical',
                         type_label='Test_Node', handle_id='4')
        core.create_node(self.neo4jdb, name='Logical Node 2', meta_type_label='Logical',
                         type_label='Test_Node', handle_id='5')

        self.assertRaises(exceptions.NoRelationshipPossible, core.create_location_relationship, self.neo4jdb,
                          location_handle_id='3', other_handle_id='4', rel_type='Has')
        self.assertRaises(exceptions.NoRelationshipPossible,core.create_location_relationship, self.neo4jdb,
                          location_handle_id='3', other_handle_id='5', rel_type='Part_of')
        self.assertRaises(exceptions.NoRelationshipPossible,core.create_location_relationship, self.neo4jdb,
                          location_handle_id='3', other_handle_id='5', rel_type='Has')





