from nnpy import AF_SP, SUB, SUB_SUBSCRIBE, PUB, Socket


class Receiver:
    def __init__(self):
        self.__socket = Socket(AF_SP, SUB)
        self.__socket.connect('ipc:///tmp/hoge.ipc')

    def __del__(self):
        self.__socket.close()

    def incoming_messages(self, topic):
        self.__socket.setsockopt(SUB, SUB_SUBSCRIBE, topic.justify())
        while True:
            # TODO: 接続切れたときの対応
            yield self.__socket.recv()


# http://stackoverflow.com/a/6798042
class Singleton(type):
    __instances = {}

    # インスタンスに()が付いたときに呼び出されるのが__call__
    # メタクラスのインスタンスはクラス
    # クラス名()で呼び出され、そのクラスのインスタンスを生成して返す
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


class Sender(metaclass=Singleton):
    def __init__(self):
        self.__socket = Socket(AF_SP, PUB)
        self.__socket.bind('ipc:///tmp/hoge.ipc')
        # 同じアドレスにbindできるのは一度に一つのSocketだけ
        # おそらくbindが完了するまでブロックされていない
        # bindの直後にsendしても届かなかった

    def __del__(self):
        self.__socket.close()

    def send(self, msg):
        self.__socket.send(msg)
