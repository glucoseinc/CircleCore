import abc


class DBWriter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def store(self, message_box, message) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def flush(self, flush_all=False) -> None:
        raise NotImplementedError
