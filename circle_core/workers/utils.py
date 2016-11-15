from nnpy import AF_SP, SUB, SUB_SUBSCRIBE, Socket
from pathlib import Path
import circle_core


class NanomsgReceiver:  # TODO: シングルトン？
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
