import unittest

from pikaconconfig import ConnectionConfig


config = 'tests/test_config.cfg'


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.config = ConnectionConfig()
        self.config.read(config)

    def test_host(self):
        self.assertEqual(self.config.host, "localhost")

    def test_port(self):
        self.assertTrue(isinstance(self.config.port, int))
        self.assertEqual(self.config.port, 5672)

    def test_username(self):
        self.assertEqual(self.config.username, "guest")

    def test_password(self):
        self.assertEqual(self.config.password, "guest")

    def test_vhost(self):
        self.assertEqual(self.config.vhost, "/")

    def test_get_exchanges(self):
        self.assertEqual(self.config.exchanges,
                         {'exchange:exchangename':
                            {'durable': False,
                             'type': 'topic',
                             'auto_delete': True}})

    def test_get_queues(self):
        self.assertEqual(self.config.queues,
                         {'queue:testqueue2':
                            {'exclusive': True, 'durable': False},
                          'queue:testqueue3':
                            {'exclusive': True, 'durable': False,
                             'arguments': {'x-message-ttl': 1800000,
                                           'x-dead-letter-exchange': 'exchangename',
                                           'x-dead-letter-routing-key': 'key3'}},
                          'queue:testqueue1': {'exclusive': True,
                                               'durable': False}})

    def test_get_bindings(self):
        self.assertEqual(self.config.bindings,
                         {'binding:testqueue1:exchangename':
                            {'routing_key': 'key1'},
                          'binding:testqueue2:exchangename':
                            {'routing_key': 'key2'},
                          'binding:testqueue3:exchangename':
                            {'routing_key': 'key3'}})
