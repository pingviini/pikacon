import logging

from pika import (PlainCredentials, ConnectionParameters, SelectConnection,
                  BasicProperties)


logger = logging.getLogger("jyu_amqplib")


class BrokerConnection(object):
    """Connection class which provides connection to AMQP broker."""

    def __init__(self, config):
        self.config = config

        credentials = PlainCredentials(username=config.username,
                                       password=config.password)

        parameters = ConnectionParameters(host=config.broker,
                                          port=int(config.port),
                                          virtual_host=config.vhost,
                                          credentials=credentials,
                                          heartbeat=True)

        parameters.heartbeat = 60
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
        self.channel.add_on_close_callback(self.on_channel_closed)

        # declare logger exchange
        callback = self.on_logging_exchange_declared
        self.channel.exchange_declare(exchange=self.config.logging_exchange,
                                      type="topic",
                                      durable=True, auto_delete=False,
                                      callback=callback)

#    def on_logging_exchange_declared(self, frame):

