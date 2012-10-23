import unittest

from pikacon import BrokerConnection


config = 'tests/test_config.cfg'


class TestBrokerConnection(unittest.TestCase):

    def setUp(self):
        self.brokerconnection = BrokerConnection(config)

    def test_connection(self):
        import pdb;pdb.set_trace()
        
        pass

