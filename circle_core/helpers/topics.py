TOPIC_LENGTH = 25


class TopicBase:
    def __metaclass__(name, *args):
        if TOPIC_LENGTH < len(name):
            raise NameError('topic name must be shorter than {} characters'.format(name))
        return type(name, *args)

    @classmethod
    def justify(cls):
        return cls.__name__.ljust(TOPIC_LENGTH)

    @classmethod
    def text(cls, msg):
        return cls.justify() + msg

    @classmethod
    def json(cls, data):
        raise NotImplementedError


class WriteDB(TopicBase):
    pass
