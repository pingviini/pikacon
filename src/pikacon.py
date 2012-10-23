import logging
import socket
import time
import random
from pika import (PlainCredentials, ConnectionParameters, SelectConnection)
from config import ConnectionConfig


logger = logging.getLogger("jyu_amqplib")


class BrokerConnection(object):
    """Connection class which provides connection to AMQP broker."""

    def __init__(self, config=None):
        self.reconnection_delay = 1.0
        self.config = ConnectionConfig(config)
        self.callbacks = self.set_callbacks()

        credentials = PlainCredentials(username=self.config.username,
                                       password=self.config.password)

        parameters = ConnectionParameters(host=self.config.host,
                                          port=int(self.config.port),
                                          virtual_host=self.config.vhost,
                                          credentials=credentials)

        parameters.heartbeat = self.config.heartbeat

        self.cancel_requests_queue = None

        self.connection = SelectConnection(parameters, self.on_connected)

    def on_connected(self, connection):
        """Called when we're connected to AMQP broker."""
        logger.info("Connected to AMQP-broker.")
        connection.channel(self.on_channel_open)

    def on_channel_open(self, new_channel):
        """Called when channel has opened"""
        logger.info("Channel to AMQP-broker opened.")
        self.channel = new_channel
#        self.channel.add_on_close_callback(self.on_channel_closed)
        self.generic_callback()

    def set_callbacks(self):
        """Set callbacks for queue factory."""
        self.exchange_callbacks = []
        self.queue_callbacks = []

        for exchange in self.config.exchanges:
            tmp = {}
            tmp['name'] = exchange
            tmp.update(self.config.exchanges[exchange])
            self.exchange_callbacks.append(tmp)

        for queue in self.config.queues:
            self.queue_callbacks.append(self.config.queues[queue])

    def get_exchange_callback(self):
        self.exchange_callbacks.popitem()

    def get_queue_callback(self):
        self.queue_callbacks.popitem()

    def generic_callback(self, channel=None, frame=None):
        """Return callback from list."""

        if channel and frame:
            # You could do error handling here
            # or add code for anonymous queue handling
            pass

        while self.exchange_callbacks:
            config = self.exchange_callbacks.pop()
            config.update({"callback": self.generic_callback})
            del config['config_for']
            self.channel.exchange_declare(**config)

        while self.queue_callbacks:
            config = self.queue_callbacks.pop()
            config.update({"callback": self.generic_callback})
            del config['config_for']
            self.channel.queue_declare(**config)

        # elif self.queue_bindings:
        #     config = self.bindings_callbacks.pop()
        #     config.update({"callback": self.generic_callback})
        #     self.channel.queue_bind(**config)

        self.loop()

    def reset_reconnection_delay(self):
        self.reconnection_delay = 1.0

    def loop(self):
        """Main loop"""

        while True:
            try:
                logger.info("Starting main loop")
                self.connection.add_on_open_callback(self.reset_reconnection_delay)
                self.connection.ioloop.start()
            except socket.error as e:
                logger.error("Connection failed or closed unexpectedly: %s", e)
            except TypeError as e:
                logger.error("Connection failed or closed unexpectedly: %s", e)
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

    def on_channel_closed(self, code, text):
        logger.warning("Channel closed with reason '%s %s'", code, text)
        self.connection.close(code, text)
