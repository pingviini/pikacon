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
import logging
import random
import socket
import sys
import time

PY2 = sys.version_info < (3,)
if PY2:
    from ConfigParser import NoOptionError  # NOQA
else:
    from configparser import NoOptionError  # NOQA

from pika import PlainCredentials, ConnectionParameters, SelectConnection

from .config import ConnectionConfig


logger = logging.getLogger("pika")
logger.setLevel(logging.DEBUG)

logger = logging.getLogger("pikacon")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)


class BrokerConnection(object):
    """Connection class which provides connection to AMQP broker."""
    exchange_callbacks = []
    queue_callbacks = []
    binding_callbacks = []
    channel = None

    def __init__(self, config, callback):
        self.closing = False
        self.channel = None
        self.connection = None
        self.reconnection_delay = 1.0
        self.caller_callback = callback

        if isinstance(config, ConnectionConfig):
            self.config = config
        else:
            self.config = ConnectionConfig()
            self.config.read(config)

        self.set_callbacks()

        credentials = PlainCredentials(**self.config.credentials)

        broker_config = self.config.broker_config
        broker_config['credentials'] = credentials

        self.parameters = ConnectionParameters(**broker_config)

        try:
            self.parameters.host = self.config.host
        except NoOptionError:
            pass

        try:
            self.parameters.heartbeat_interval = int(
                self.config.heartbeat_interval)
        except NoOptionError:
            pass

        self.connect()

    def connect(self):
        """

        :param parameters:
        :return:
        """
        self.connection = SelectConnection(self.parameters, self.on_connected,
                                           stop_ioloop_on_close=False)

    def on_connected(self, connection):
        """Called when we're connected to AMQP broker."""
        print("Connected to AMQP-broker.")
        self.add_on_connection_close_callback()
        connection.channel(self.on_channel_open)

    def add_on_connection_close_callback(self):
        """This method adds an on close callback that will be invoked by pika
        when RabbitMQ closes the connection to the publisher unexpectedly.

        """
        print('Adding connection close callback')
        self.connection.add_on_close_callback(self.on_connection_closed)

    def on_connection_closed(self, connection, reply_code, reply_text):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param int reply_code: The server provided reply_code if given
        :param str reply_text: The server provided reply_text if given

        """
        self.channel = None
        if self.closing:
            self.connection.ioloop.stop()
        else:
            print('Connection closed, reopening in 5 seconds: (%s) %s',
                  reply_code, reply_text)
            self.connection.add_timeout(5, self.reconnect)

    def on_channel_open(self, new_channel):
        """Called when channel has opened"""
        logger.info("Channel to AMQP-broker opened.")
        self.channel = new_channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        self.generic_callback()

    def set_callbacks(self):
        """Set callbacks for queue factory."""

        for exchange in self.config.exchanges:
            tmp = {'exchange': exchange}
            tmp.update(self.config.exchanges[exchange])
            self.exchange_callbacks.append(tmp)

        for queue in self.config.queues:
            tmp = {'queue': queue}
            tmp.update(self.config.queues[queue])
            self.queue_callbacks.append(tmp)

        for binding in self.config.bindings:
            tmp = {'binding': binding}
            tmp.update(self.config.bindings[binding])
            self.binding_callbacks.append(tmp)

    def generic_callback(self, channel=None, frame=None):
        """Create exchanges, queues and bindings."""

        if channel and frame:
            # You could do error handling here
            # or add code for anonymous queue handling
            pass

        if self.exchange_callbacks:
            config = self.exchange_callbacks.pop()
            config['exchange'] = config['exchange'].split(':', 1)[-1]
            logger.info("Creating exchange %s." % config['exchange'])
            config.update({"callback": self.generic_callback})
            self.channel.exchange_declare(**config)

        elif self.queue_callbacks:
            config = self.queue_callbacks.pop()
            config['queue'] = config['queue'].split(':', 1)[-1]
            logger.info("Creating queue %s." % config['queue'])
            config.update({"callback": self.generic_callback})
            self.channel.queue_declare(**config)

        elif self.binding_callbacks:
            config = self.binding_callbacks.pop()
            binding = config['binding'].split(':')
            del config['binding']
            config['exchange'] = binding[-1]
            config['queue'] = binding[1]
            logger.info("Creating binding (%s -> %s) with routing key %s" % (
                config['exchange'], config['queue'],
                config['routing_key']))
            config.update({"callback": self.generic_callback})
            self.channel.queue_bind(**config)

        else:
            logger.info("RabbitMQ exchanges, queues and bindings are now "
                        "configured.")
            self.caller_callback()

    def reset_reconnection_delay(self, *args):
        self.reconnection_delay = 1.0

    def loop(self):
        """Main loop"""

        while True:
            try:
                logger.info("Starting main loop")
                self.connection.add_on_open_callback(
                    self.reset_reconnection_delay)
                self.connection.ioloop.start()
            except socket.error as e:
                logger.error("Connection failed or closed unexpectedly: %s", e,
                             exc_info=True)
            except TypeError as e:
                logger.error("Connection failed or closed unexpectedly: %s", e,
                             exc_info=True)
            except KeyboardInterrupt:
                self.connection.close()
                self.connection.ioloop.start()
                break
            finally:
                self.reconnection_delay *= (random.random() * 0.5) + 1
                self.reconnection_delay = min(self.reconnection_delay, 60.0)
                logger.info("Trying reconnection in %s seconds",
                            self.reconnection_delay)
                time.sleep(self.reconnection_delay)

    def on_channel_closed(self, channel, code, text):
        logger.warning("Channel closed with reason '%s %s'",
                       code, text)
        self.connection.close(code, text)

    def reconnect(self):
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.

        """
        # This is the old connection IOLoop instance, stop its ioloop
        self.connection.ioloop.stop()

        if not self.closing:
            # Create a new connection
            self.connect()

            # There is now a new connection, needs a new ioloop to run
            self.connection.ioloop.start()

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        print('Adding consumer cancellation callback')
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """
        Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        print('Consumer was cancelled remotely, shutting down: %r' %
              method_frame)
        if self.channel:
            self.channel.close()
