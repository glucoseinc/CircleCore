import abc


class DBWriter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def store(self, message_box, message) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self, flush_all=False) -> None:
        raise NotImplementedError
