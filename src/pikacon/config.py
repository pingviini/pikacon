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
import sys

PY2 = sys.version_info < (3,)
if PY2:
    from ConfigParser import SafeConfigParser as ConfigParser, NoOptionError
else:
    from configparser import ConfigParser, NoOptionError


logger = logging.getLogger("pikacon")


class ConnectionConfig(ConfigParser):
    """
    ConnectionConfig provides all the attributes pika needs for creating
    connection, exchanges, queues and bindings.
    """

    @property
    def broker_config(self):
        config = {}
        converted = []
        convert_to_int = ["port", "heartbeat_interval", "channel_max",
                          "frame_max", "connection_attempts", "ssl_port"]
        convert_to_float = ["retry_delay", "socket_timeout"]
        convert_to_bool = ["ssl", "backpressure_detection"]

        for option in convert_to_int:
            try:
                config[option] = self.getint("broker", option)
                converted.append(option)
            except NoOptionError:
                pass

        for option in convert_to_float:
            try:
                config[option] = self.getfloat("broker", option)
                converted.append(option)
            except NoOptionError:
                pass

        for option in convert_to_bool:
            try:
                config[option] = self.getfloat("broker", option)
                converted.append(option)
            except NoOptionError:
                pass

        for option in self.options("broker"):
            if not option in converted and\
                    option not in ["username", "password"]:
                if option == "ssl_options":
                    ssl_options = dict(self.items(self.get('broker',
                                                           'ssl_options')))
                    config[option] = ssl_options
                else:
                    config[option] = self.get("broker", option)

        return config

    @property
    def credentials(self):
        """Return dict containing username and password."""
        return {'username': self.username, 'password': self.password}

    @property
    def host(self):
        return self.get("broker", "host")

    @property
    def port(self):
        return self.getint("broker", "port")

    @property
    def username(self):
        try:
            return self.get("broker", "username")
        except NoOptionError:
            return 'guest'

    @property
    def password(self):
        try:
            return self.get("broker", "password")
        except NoOptionError:
            return 'guest'

    @property
    def virtual_host(self):
        return self.get("broker", "virtual_host")

    @property
    def heartbeat(self):
        return self.getint("broker", "heartbeat")

    @property
    def channel_max(self):
        return self.getint("broker", "channel_max")

    @property
    def frame_max(self):
        return self.getint("broker", "frame_max")

    @property
    def ssl(self):
        return self.getbool("broker", "ssl")

    @property
    def ssl_options(self):
        return self.getbool("broker", "ssl_options")

    @property
    def connection_attempts(self):
        return self.getint("broker", "connection_attempts")

    @property
    def retry_delay(self):
        return self.getint("broker", "retry_delay")

    @property
    def socket_timeout(self):
        return self.getint("broker", "socket_timeout")

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

    def get_config(self, section_name):
        """Return list of sections which are for specified config"""

        sections = {}

        for section in self.sections():
            try:
                assert(section != "broker")
                assert(section.split(':', 1)[0] == section_name)
                if section_name == 'queue':
                    # skip arguments in here
                    assert(len(section.split(':')) < 3)
                assert(section.split(':', 1)[0] == section_name)

                options = self.options(section)
                items = {}

                if 'arguments' in options:
                    arguments_name = self.get(section, 'arguments')
                    arguments = self.get_arguments(arguments_name)
                    items['arguments'] = arguments
                    options.remove('arguments')

                for option in options:
                    try:
                        items[option] = self.getboolean(section, option)
                    except ValueError:
                        items[option] = self.get(section, option)

                sections[section] = items
            except NoOptionError:
                # Config file has configuration which doesn't belong to
                # pikacon so we ignore it.
                pass
            except AssertionError:
                # We're parsing broker section which will be ignored too.
                pass

        return sections

    @property
    def get_exchanges(self):
        """Returns list of Exchange objects."""
        return

    def get_arguments(self, name):
        """Return dict of arguments for section"""

        kw = {}
        options = self.options(name)

        for option in options:
            try:
                kw[option] = self.getint(name, option)
            except ValueError:
                kw[option] = self.get(name, option)

        return kw
