# -*- coding: utf-8 -*-

from __future__ import absolute_import

from norduniclient.testing import Neo4jTestCase
from norduniclient import core
from norduniclient import exceptions
from norduniclient import models

__author__ = 'lundberg'


class ModelsTests(Neo4jTestCase):

    def setUp(self):
        super(ModelsTests, self).setUp()
        q = """
        // Create nodes
        CREATE (router1:Node:Physical:Router{name:'Router1', handle_id:'1'}),
        (port1:Node:Physical:Port{name:'Port1', handle_id:'2'}),
        (unit1:Node:Logical:Unit{name:'Unit1', handle_id:'3'}),
        (port6:Node:Physical:Port{name:'Port6', handle_id:'4'}),
        (unit2:Node:Logical:Unit{name:'Unit2', handle_id:'5'}),
        (provider1:Node:Relation:Provider{name:'Provider1', handle_id:'6'}),
        (peering_group1:Node:Logical:Peering_Group{name:'Peering Group1', handle_id:'7'}),
        (peering_partner1:Node:Relation:Peering_Partner{name:'Peering Partner1', handle_id:'8'}),
        (service2:Node:Logical:Service{name:'Service2', handle_id:'9'}),
        (service3:Node:Logical:Service{name:'Service3', handle_id:'10'}),
        (site1:Node:Location:Site{name:'Site1', handle_id:'11'}),
        (rack1:Node:Location:Rack{name:'Rack1', handle_id:'12'}),
        (optical_node1:Node:Physical:Optical_Node{name:'Optical Node1', handle_id:'13'}),
        (port2:Node:Physical:Port{name:'Port2', handle_id:'14', description:'This is a port'}),
        (rack2:Node:Location:Rack{name:'Rack2', handle_id:'15'}),
        (optical_node2:Node:Physical:Optical_Node{name:'Optical Node2', handle_id:'16'}),
        (port3:Node:Physical:Port{name:'Port3', handle_id:'17'}),
        (site2:Node:Location:Site{name:'Site2', handle_id:'18'}),
        (rack3:Node:Location:Rack{name:'Rack3', handle_id:'19'}),
        (optical_path1:Node:Logical:Optical_Path{name:'Optical Path1', handle_id:'20'}),
        (optical_link1:Node:Logical:Optical_Link{name:'Optical Link1', handle_id:'21'}),
        (optical_link2:Node:Logical:Optical_Link{name:'Optical Link2', handle_id:'22'}),
        (odf1:Node:Physical:ODF{name:'ODF1', handle_id:'23'}),
        (port4:Node:Physical:Port{name:'Port4', handle_id:'24'}),
        (odf2:Node:Physical:ODF{name:'ODF2', handle_id:'25'}),
        (port5:Node:Physical:Port{name:'Port5', handle_id:'26'}),
        (port7:Node:Physical:Port{name:'Port7', handle_id:'27'}),
        (cable1:Node:Physical:Cable{name:'Cable1', handle_id:'28'}),
        (cable2:Node:Physical:Cable{name:'Cable2', handle_id:'29'}),
        (cable3:Node:Physical:Cable{name:'Cable3', handle_id:'30'}),
        (cable4:Node:Physical:Cable{name:'Cable4', handle_id:'31'}),
        (host1:Node:Physical:Host{name:'Host1', handle_id:'32'}),
        (host2:Node:Logical:Host{name:'Host2', handle_id:'33'}),
        (customer1:Node:Relation:Customer{name:'Customer1', handle_id:'34'}),
        (customer2:Node:Relation:Customer{name:'Customer2', handle_id:'35'}),
        (customer3:Node:Relation:Customer{name:'Customer3', handle_id:'36'}),
        (customer4:Node:Relation:Customer{name:'Customer4', handle_id:'37'}),
        (service4:Node:Logical:Service{name:'Service4', handle_id:'38'}),

        // Create relationships
        (router1)-[:Has]->(port1),
        (unit1)-[:Part_of]->(port1),
        (router1)-[:Has]->(port6),
        (unit2)-[:Part_of]->(port6),
        (provider1)-[:Owns]->(router1),
        (provider1)-[:Provides]->(peering_group1),
        (peering_partner1)-[:Uses]->(peering_group1),
        (peering_group1)-[:Depends_on]->(unit1),
        (site1)-[:Has]->(rack1),
        (router1)-[:Located_in]->(rack1),
        (provider1)-[:Responsible_for]->(rack1),
        (optical_node1)-[:Has]->(port2),
        (site1)-[:Has]->(rack2),
        (optical_node1)-[:Located_in]->(rack2),
        (optical_node2)-[:Has]->(port3),
        (site2)-[:Has]->(rack3),
        (optical_node2)-[:Located_in]->(rack3),
        (provider1)-[:Provides]->(optical_path1),
        (service2)-[:Depends_on]->(optical_path1),
        (service3)-[:Depends_on]->(unit2),
        (odf1)-[:Located_in]->(rack2),
        (odf1)-[:Has]->(port4),
        (odf2)-[:Located_in]->(rack3),
        (odf2)-[:Has]->(port5),
        (odf2)-[:Has]->(port7),
        (port4)<-[:Connected_to]-(cable1)-[:Connected_to]->port2,
        (port5)<-[:Connected_to]-(cable2)-[:Connected_to]->port3,
        (port4)<-[:Connected_to]-(cable3)-[:Connected_to]->port5,
        (port6)<-[:Connected_to]-(cable4)-[:Connected_to]->port7,
        (optical_link1)-[:Depends_on]->(port2),
        (optical_link2)-[:Depends_on]->(port3),
        (optical_link1)-[:Depends_on]->(port4),
        (optical_link2)-[:Depends_on]->(port5),
        (optical_path1)-[:Depends_on]->(port4),
        (optical_path1)-[:Depends_on]->(port5),
        (optical_path1)-[:Depends_on]->(optical_link1),
        (optical_path1)-[:Depends_on]->(optical_link2),
        (provider1)-[:Owns]->(host1),
        (host2)-[:Depends_on]->(host1),
        (customer1)-[:Uses]->(host2),
        (customer2)-[:Uses]->(service2),
        (customer2)-[:Uses]->(service3),
        (customer3)-[:Uses]->(service3)
        """
        with self.neo4jdb.transaction as w:
            w.execute(q).fetchall()

    def test_base_node_model(self):
        node_model_1 = core.get_node_model(self.neo4jdb, handle_id='1')
        node_model_2 = core.get_node_model(self.neo4jdb, handle_id='2')

        self.assertIsNotNone(str(node_model_1))
        self.assertIsNotNone(repr(node_model_1))

        self.assertEquals(node_model_1, node_model_1)
        self.assertGreater(node_model_2, node_model_1)
        self.assertLess(node_model_1, node_model_2)

        self.assertEqual(node_model_1.handle_id, '1')
        self.assertIn(node_model_1.meta_type, core.META_TYPES)
        self.assertIsInstance(node_model_1.labels, list)
        self.assertIsInstance(node_model_1.data, dict)
        self.assertIsInstance(node_model_1.incoming, dict)
        self.assertIsInstance(node_model_1.outgoing, dict)
        self.assertIsInstance(node_model_1.relationships, dict)

    def test_add_label(self):
        node_model_1 = core.get_node_model(self.neo4jdb, handle_id='1')
        initial_labels = node_model_1.labels
        node_model_1.add_label('Test_Label')
        node_model_1 = node_model_1.reload()
        new_labels = node_model_1.labels
        expected_labels = initial_labels + ['Test_Label']
        self.assertEqual(new_labels, expected_labels)

    def test_remove_label(self):
        node_model_1 = core.get_node_model(self.neo4jdb, handle_id='1')
        initial_labels = node_model_1.labels
        node_model_1 = node_model_1.add_label('Test_Label')
        new_labels = node_model_1.labels
        expected_labels = initial_labels + ['Test_Label']
        self.assertEqual(new_labels, expected_labels)
        node_model_1 = node_model_1.remove_label('Test_Label')
        new_labels = node_model_1.labels
        self.assertEqual(new_labels, initial_labels)

    def test_change_meta_type(self):
        node_model_1 = core.get_node_model(self.neo4jdb, handle_id='1')
        self.assertEqual(node_model_1.meta_type, 'Physical')
        node_model_1 = node_model_1.change_meta_type('Logical')
        self.assertEqual(node_model_1.meta_type, 'Logical')

    def test_switch_type(self):
        node_model_1 = core.get_node_model(self.neo4jdb, handle_id='1')
        self.assertIn('Router', node_model_1.labels)
        self.assertIsInstance(node_model_1, models.RouterModel)
        node_model_1 = node_model_1.switch_type(old_type='Router', new_type='Host')
        self.assertNotIn('Router', node_model_1.labels)
        self.assertIn('Host', node_model_1.labels)
        self.assertIsInstance(node_model_1, models.HostModel)

    def test_delete(self):
        node_model_1 = core.get_node_model(self.neo4jdb, handle_id='1')
        node_model_1.delete()
        self.assertRaises(exceptions.NodeNotFound, core.get_node_model, self.neo4jdb, handle_id='1')

    def test_base_relationship_model(self):
        node_model_1 = core.get_node_model(self.neo4jdb, handle_id='1')
        outgoing_relationships = node_model_1.outgoing
        self.assertGreater(len(outgoing_relationships), 0)

        for rel_type, relationships in outgoing_relationships.items():
            self.assertIsNotNone(rel_type)
            for item in relationships:
                relationship_model = core.get_relationship_model(self.neo4jdb, item['relationship_id'])
                self.assertIsNotNone(str(relationship_model))
                self.assertIsNotNone(repr(relationship_model))
                self.assertIsNotNone(relationship_model.type)
                self.assertIsInstance(relationship_model.id, int)
                self.assertIsInstance(relationship_model.data, dict)
                self.assertEqual(relationship_model.start, node_model_1.handle_id)
                self.assertEqual(relationship_model.end, item['node'].handle_id)

    def test_get_location_path(self):
        # Model with location
        router1 = core.get_node_model(self.neo4jdb, handle_id='1')
        location_path = router1.get_location_path()
        self.assertEqual(location_path['location_path'][0]['name'], 'Site1')
        self.assertEqual(location_path['location_path'][1]['name'], 'Rack1')

        # Model without location
        provider1 = core.get_node_model(self.neo4jdb, handle_id='6')
        location_path = provider1.get_location_path()
        self.assertEqual(location_path['location_path'], [])

    def test_get_location(self):
        # Model with location
        router1 = core.get_node_model(self.neo4jdb, handle_id='1')
        location = router1.get_location()
        self.assertIsInstance(location['Located_in'][0]['node'], models.LocationModel)
        self.assertIsInstance(location['Located_in'][0]['relationship_id'], int)

        # Model without location
        provider1 = core.get_node_model(self.neo4jdb, handle_id='6')
        location = provider1.get_location()
        self.assertIsNone(location.get('Located_in'))

    def test_get_placement_path(self):
        # Models with placement path
        port1 = core.get_node_model(self.neo4jdb, handle_id='2')
        placement_path = port1.get_placement_path()
        self.assertEqual(placement_path['placement_path'][0]['name'], 'Router1')

        unit1 = core.get_node_model(self.neo4jdb, handle_id='3')
        placement_path = unit1.get_placement_path()
        self.assertEqual(placement_path['placement_path'][0]['name'], 'Router1')
        self.assertEqual(placement_path['placement_path'][1]['name'], 'Port1')

        # Model without placement path
        provider1 = core.get_node_model(self.neo4jdb, handle_id='6')
        location_path = provider1.get_placement_path()
        self.assertEqual(location_path['placement_path'], [])

    def test_get_child_form_data(self):
        optical_node1 = core.get_node_model(self.neo4jdb, handle_id='13')
        child_form_data = optical_node1.get_child_form_data(node_type='Port')
        self.assertEqual(child_form_data[0]['handle_id'], '14')
        self.assertEqual(child_form_data[0]['name'], 'Port2')
        self.assertEqual(child_form_data[0]['description'], 'This is a port')
        self.assertEqual(child_form_data[0]['labels'], [u'Node', u'Physical', u'Port'])

    def test_get_relations(self):
        host1 = core.get_node_model(self.neo4jdb, handle_id='32')
        relations = host1.get_relations()
        self.assertEqual(host1.meta_type, 'Physical')
        self.assertIsInstance(relations['Owns'][0]['node'], models.RelationModel)

        host2 = core.get_node_model(self.neo4jdb, handle_id='33')
        relations = host2.get_relations()
        self.assertEqual(host2.meta_type, 'Logical')
        self.assertIsInstance(relations['Uses'][0]['node'], models.RelationModel)

        optical_path1 = core.get_node_model(self.neo4jdb, handle_id='20')
        relations = optical_path1.get_relations()
        self.assertIsInstance(relations['Provides'][0]['node'], models.RelationModel)

        rack1 = core.get_node_model(self.neo4jdb, handle_id='12')
        relations = rack1.get_relations()
        self.assertIsInstance(relations['Responsible_for'][0]['node'], models.RelationModel)

    def test_get_dependencies(self):
        service2 = core.get_node_model(self.neo4jdb, handle_id='9')
        dependencies = service2.get_dependencies()
        self.assertEqual(len(dependencies['Depends_on']), 1)
        self.assertEqual(dependencies['Depends_on'][0]['node'].handle_id, '20')
        self.assertIsInstance(dependencies['Depends_on'][0]['node'], models.OpticalPathModel)

    def test_get_dependents(self):
        optical_path1 = core.get_node_model(self.neo4jdb, handle_id='20')
        dependents = optical_path1.get_dependents()
        self.assertEqual(len(dependents['Depends_on']), 1)
        self.assertEqual(dependents['Depends_on'][0]['node'].handle_id, '9')
        self.assertIsInstance(dependents['Depends_on'][0]['node'], models.ServiceModel)

    def test_get_dependent_as_types(self):
        optical_link1 = core.get_node_model(self.neo4jdb, handle_id='21')
        dependents = optical_link1.get_dependent_as_types()
        self.assertEqual(dependents['direct'][0]['name'], 'Optical Path1')
        self.assertEqual(dependents['links'], [])
        self.assertEqual(dependents['oms'], [])
        self.assertEqual(dependents['paths'][0]['name'], 'Optical Path1')
        self.assertEqual(dependents['services'][0]['name'], 'Service2')

    def test_get_dependencies_as_types(self):
        service2 = core.get_node_model(self.neo4jdb, handle_id='9')
        dependencies = service2.get_dependencies_as_types()
        self.assertEqual(dependencies['direct'][0]['name'], 'Optical Path1')
        self.assertEqual(len(dependencies['links']), 2)
        self.assertEqual(dependencies['oms'], [])
        self.assertEqual(dependencies['paths'][0]['name'], 'Optical Path1')
        self.assertEqual(dependencies['services'], [])

    def test_get_ports(self):
        cable1 = core.get_node_model(self.neo4jdb, handle_id='28')
        ports = cable1.get_ports()
        self.assertIsInstance(ports, list)
        self.assertEqual(len(ports), 2)

    def test_get_part_of_logical_model(self):
        unit1 = core.get_node_model(self.neo4jdb, handle_id='3')
        part_of = unit1.get_part_of()
        self.assertEqual(part_of['Part_of'][0]['node'].handle_id, '2')

    def test_set_user_logical_model(self):
        customer4 = core.get_node_model(self.neo4jdb, handle_id='37')
        service4 = core.get_node_model(self.neo4jdb, handle_id='38')

        result = service4.set_user(customer4.handle_id)
        self.assertEqual(result['Uses'][0]['created'], True)
        relations = service4.get_relations()
        self.assertEqual(len(relations['Uses']), 1)
        self.assertEqual(relations['Uses'][0]['node'].handle_id, customer4.handle_id)

        # Do not accept duplicates
        result = service4.set_user(customer4.handle_id)
        self.assertEqual(result['Uses'][0]['created'], False)
        relations = service4.get_relations()
        self.assertEqual(len(relations['Uses']), 1)

    def test_set_provider_logical_model(self):
        provider_1 = core.get_node_model(self.neo4jdb, handle_id='6')
        service4 = core.get_node_model(self.neo4jdb, handle_id='38')

        result = service4.set_provider(provider_1.handle_id)
        self.assertEqual(result['Provides'][0]['created'], True)
        relations = service4.get_relations()
        self.assertEqual(len(relations['Provides']), 1)
        self.assertEqual(relations['Provides'][0]['node'].handle_id, provider_1.handle_id)

        # Do not accept duplicates
        result = service4.set_provider(provider_1.handle_id)
        self.assertEqual(result['Provides'][0]['created'], False)
        relations = service4.get_relations()
        self.assertEqual(len(relations['Provides']), 1)

    def test_set_dependency_logical_model(self):
        optical_path1 = core.get_node_model(self.neo4jdb, handle_id='20')
        service4 = core.get_node_model(self.neo4jdb, handle_id='38')

        result = service4.set_dependency(optical_path1.handle_id)
        self.assertEqual(result['Depends_on'][0]['created'], True)
        relations = service4.get_dependencies()
        self.assertEqual(len(relations['Depends_on']), 1)
        self.assertEqual(relations['Depends_on'][0]['node'].handle_id, optical_path1.handle_id)

        # Do not accept duplicates
        result = service4.set_dependency(optical_path1.handle_id)
        self.assertEqual(result['Depends_on'][0]['created'], False)
        relations = service4.get_dependencies()
        self.assertEqual(len(relations['Depends_on']), 1)

    # TODO: EquipmentModel get_ports should probably work as CommonQueries get_ports
    def test_get_ports_equipment_model(self):
        odf1 = core.get_node_model(self.neo4jdb, handle_id='23')
        ports = odf1.get_ports()
        self.assertIsInstance(ports, dict)
        self.assertEqual(len(ports['Has']), 1)
        for rel_type, items in ports.items():
            self.assertEqual(len(items), 1)
