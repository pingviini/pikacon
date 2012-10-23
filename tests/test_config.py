import unittest
from config import ConnectionConfig


config = 'tests/test_config.cfg'


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.config = ConnectionConfig(config)

    def test_host(self):
        self.assertEqual(self.config.host, "localhost")

    def test_port(self):
        self.assertEqual(self.config.port, "5432")

    def test_username(self):
        self.assertEqual(self.config.username, "guest")

    def test_password(self):
        self.assertEqual(self.config.password, "guest")

    def test_vhost(self):
        self.assertEqual(self.config.vhost, "/")

    def test_get_exchanges(self):
        self.assertEqual(self.config.exchanges,
                         [{'exchange': {'config_for': 'exchange',
                                        'durable': False,
                                        'type': 'topic',
                                        'auto_delete': True}}])

    def test_get_queues(self):
        self.assertEqual(self.config.queues,
                         [{'queue1': {'config_for': 'queue',
                                      'name': 'testqueue-1',
                                      'durable': False,
                                      'exclusive': True}},
                          {'queue2': {'config_for': 'queue',
                                      'name': 'testqueue-2',
                                      'durable': False,
                                      'exclusive': True}}])
