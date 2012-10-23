Introduction
============

Pikacon is a helper library which will reduce the amount of boilerplate your
software needs when it is using pika for creating connection to broker and
declaring exchanges and queues.

Requirements
------------

* python 2.7
* pika

Usage
-----

Pikacon provides helper class which can be imported to your program. Class
takes a path to .ini-style config file as a parameter and creates connection,
exchanges and queues automatically from there. All you need to provide is a
proper config.

Config
------

Pikacon uses Pythons ConfigParser to get config for connection, exchanges and
queues.

Below is an example of config file::

    [broker]
    host = localhost
    port = 5432
    username = guest
    password = guest

    [exchange1]
    config_for = exchange
    type = fanout
    durable = False
    auto_delete = True

    [queue1]
    config_for = queue
    name = queue1
    durable = False
    exclusive = True

In above example config_for tells the parser what kind of config this section
contains. Rest of the parameters are regular pika parameters.
