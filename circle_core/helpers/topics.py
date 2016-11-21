TOPIC_LENGTH = 25  # Topic name must be shorter than this value


class TopicBase:
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
