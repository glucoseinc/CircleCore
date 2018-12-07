import abc


class WriterBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def store(self, message_box, message):
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self, flush_all=False):
        raise NotImplementedError
