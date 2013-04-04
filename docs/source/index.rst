.. Pikacon documentation master file, created by
   sphinx-quickstart on Wed Apr  3 22:19:40 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pikacon's documentation!
===================================

Pikacon is a helper library which will reduce the amount of boilerplate your
software needs when it is using pika for creating connection to broker and
declaring exchanges and queues.

Pikacon provides helper class (ClassName) which can be imported to your
program. Class takes a path to ini-style config file as a parameter and creates
connection, exchanges, queues and bindings automatically from there. All you
need to provide is a proper config.

Contents:

.. toctree::
   :maxdepth: 2

   Configuration <configuration>
   Integration example <example>
   Source code <source>
