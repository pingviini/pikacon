callbacks = []

def generic_callback(channel, frame):
    return callback.sop()(channel, frame)


def queue_factory(channel, callback, config, queue_params):
    """Queue factory"""

    def declare_queue(channel, frame):
        channel.queue_declare(queue=queue_params['name'],
                              durable=queue_params['durable'],
                              auto_delete=queue_params['auto_delete'],
                              exclusive=queue_params['exclusive'],
                              callback=generic_callback)

    return declare_queue
