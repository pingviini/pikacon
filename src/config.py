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
        return self.parser.get("broker", "port")

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

    def get_config(self, config_for):
        """Return list of sections which are for specified config"""

        sections = {}

        for section in self.parser.sections():
            if section != "broker" and\
                self.parser.get(section, "config_for") == config_for:

                options = self.parser.options(section)
                items = {}

                for option in options:
                    try:
                        items[option] = self.parser.getboolean(section, option)
                    except ValueError:
                        items[option] = self.parser.get(section, option)

                sections[section] = items

        return sections
