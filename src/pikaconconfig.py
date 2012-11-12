import logging
import ConfigParser


logger = logging.getLogger("pikacon")


class ConnectionConfig(object):

    def __init__(self, config):
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(config)

    @property
    def host(self):
        return self.parser.get("broker", "host")

    @property
    def port(self):
        return self.parser.getint("broker", "port")

    @property
    def username(self):
        return self.parser.get("broker", "username")

    @property
    def password(self):
        return self.parser.get("broker", "password")

    @property
    def vhost(self):
        return self.parser.get("broker", "vhost")

    @property
    def heartbeat(self):
        return self.parser.get("broker", "heartbeat")

    @property
    def exchanges(self):
        """Return list of exchanges"""
        return self.get_config("exchange")

    @property
    def queues(self):
        """Return list of queues"""
        return self.get_config("queue")

    @property
    def bindings(self):
        """Return list of bindings"""
        return self.get_config("binding")

    def get_config(self, config_for):
        """Return list of sections which are for specified config"""

        sections = {}

        for section in self.parser.sections():
            try:
                assert(section != "broker")
                assert(self.parser.get(section, "config_for") == config_for)

                options = self.parser.options(section)
                items = {}

                if 'arguments' in options:
                    arguments_name = self.parser.get(section, 'arguments')
                    arguments = self.get_arguments(arguments_name)
                    items['arguments'] = arguments
                    options.remove('arguments')

                for option in options:
                    try:
                        items[option] = self.parser.getboolean(section, option)
                    except ValueError:
                        items[option] = self.parser.get(section, option)

                sections[section] = items
            except ConfigParser.NoOptionError:
                # Config file has configuration which doesn't belong to
                # pikacon so we ignore it.
                pass
            except AssertionError:
                # We're parsing broker section which will be ignored too.
                pass

        return sections

    def get_arguments(self, name):
        """Return dict of arguments for section"""

        kw = {}
        options = self.parser.options(name)

        for option in options:
            try:
                kw[option] = self.parser.getint(name, option)
            except ValueError:
                kw[option] = self.parser.get(name, option)

        return kw
