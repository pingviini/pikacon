import unittest
from pikacon import BrokerConnection
from config import ConnectionConfig


conf = 'tests/test_config.cfg'


class MockBrokerConnection(BrokerConnection):

    def __init__(self, config):
        self.config = ConnectionConfig(config)
        self.set_callbacks()


class TestPikaconCallbacks(unittest.TestCase):

    def test_callbacks(self):
        connection = MockBrokerConnection(conf)
        self.assertTrue(len(connection.exchange_callbacks) == 1)
        self.assertTrue(len(connection.queue_callbacks) == 2)
