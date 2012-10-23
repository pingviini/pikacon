import ConfigParser


def generate_config():
    config = ConfigParser.SafeConfigParser()
    config.add_section('broker')
    config.set('broker', 'host', 'localhost')
    config.set('broker', 'port', '5432')
    config.set('broker', 'vhost', '/')
    config.set('broker', 'username', 'guest')
    config.set('broker', 'password', 'guest')

    config.add_section('exchange1')
    config.set('exchange1', 'config_for', 'exchange')
    config.set('exchange1', 'type', 'fanout')
    config.set('exchange1', 'auto_delete', 'True')
    config.set('exchange1', 'durable', 'False')

    config.add_section('queue1')
    config.set('queue1', 'config_for', 'queue')
    config.set('queue1', 'name', 'queue1')
    config.set('queue1', 'exclusive', 'True')
    config.set('queue1', 'durable', 'False')

    config.add_section('queue2')
    config.set('queue2', 'config_for', 'queue')
    config.set('queue2', 'name', 'queue2')
    config.set('queue2', 'exclusive', 'True')
    config.set('queue2', 'durable', 'False')

    return config
