"""
This file is part of pikacon.

Pikacon is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pikacon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pikacon.  If not, see <http://www.gnu.org/licenses/>.
"""
import unittest

from pikacon.config import ConnectionConfig

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
        self.assertEqual(self.config.virtual_host, "/")

    def test_get_exchanges(self):
        self.assertEqual(self.config.exchanges,
                         {'exchange:exchangename':
                            {'durable': False,
                             'type': 'topic',
                             'auto_delete': True}})

    def test_get_queues(self):
        self.assertEqual(
            self.config.queues,
            {'queue:testqueue2': {
                'exclusive': True,
                'durable': False},
             'queue:testqueue3': {
                 'exclusive': True,
                 'durable': False,
                 'arguments': {'x-message-ttl': 1800000,
                               'x-dead-letter-exchange': 'exchangename',
                               'x-dead-letter-routing-key': 'key3'}},
             'queue:testqueue1': {
                 'exclusive': True,
                 'durable': False}})

    def test_get_bindings(self):
        self.assertEqual(
            self.config.bindings,
            {'binding:testqueue1:exchangename': {'routing_key': 'key1'},
             'binding:testqueue2:exchangename': {'routing_key': 'key2'},
             'binding:testqueue3:exchangename': {'routing_key': 'key3'}})
