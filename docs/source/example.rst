Pikacon usage example
=====================

::

    from pikacon.pikacon import BrokerConnection

    class PikaconExample(object):

        def __init__(self):
            self.broker = BrokerConnection(
                '/path/to/config.cfg',
                callback=self.broker_ready_callback)

        def broker_ready_callback(self):
            """Do something with the broker."""
            self.broker.channel.basic_consume(self.handle_messages,
                                              'queue')


Yes. Above is full example of working code which sets up connections,
channels, exchanges, queues and bindings assuming they have been configured
in /path/to/congfig.cfg. You can start using self.broker as you would use
pika.
