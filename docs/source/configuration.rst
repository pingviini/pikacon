Configuration
=============

Pikacon uses Pythons ConfigParser to get config for connection, exchanges and
queues.

Broker
------

Broker is configured as in above example. Section name is broker and options
are regular pika parameters for broker. If you want to configure ssl_options
create new section for those and refer that section name in broker options.
Eg.::

    [broker]
    ...
    ssl = True
    ssl_options = my_ssl_options

    [my_ssl_options]
    ...

Exchange
--------

Section name for exchange consists of two parts divided by ':'. First part is
'exchange' and second part is the name of the exchange. Eg.::

    [exchange:myexchange]
    ...

The actual options below exchange section are normal key = value parameters
which are used in pika.

Binding
-------

The name of the binding section consists three parts divided by ':'. First
part is always 'binding'. Second part is the name of the queue we're binding.
Third part is name of the exchange where we're binding the queue. Eg.::

    [binding:myqueue:myexchange]

The actual options below binding section are normal key = value parameters
which are used in pika.

Processing order
----------------

Pikacon's processing order is following:

1. Connection
2. Channel
3. Exchanges
4. Queues
5. Bindings

Complete configuration example
------------------------------
::

    [broker]
    host = localhost
    port = 5672
    username = guest
    password = guest
    virtual_host = /
    heartbeat = 60

    [exchange:exchangename]
    type = direct
    durable = False
    auto_delete = True

    [queue:testqueue1]
    durable = True
    exclusive = False

    [queue:testqueue2]
    durable = False
    exclusive = False

    [queue:testqueue3]
    durable = True
    exclusive = False
    arguments = queue:testqueue3:arguments

    [queue:testqueue4]
    durable = True
    exclusive = False

    [queue:testqueue3:arguments]
    x-message-ttl = 1800000
    x-dead-letter-exchange = exchangename
    x-dead-letter-routing-key = key4

    [binding:testqueue1:exchangename]
    routing_key = key1

    [binding:testqueue2:exchangename]
    routing_key = key2

    [binding:testqueue3:exchangename]
    routing_key = key3

    [binding:testqueue4:exchangename]
    routing_key = key4

Above example configures connection to broker at localhost. It defines one
direct exchange called exchangename and four queues called testqueue1,
testqueue2, testqueue3 and testqueue4. Testqueue3 has extra arguments which
define dead letter exchange. All queues are bound to our only exchange with
routingkeys key1, key2, key3 and key4.
