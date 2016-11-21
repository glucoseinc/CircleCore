"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""

TOPIC_LENGTH = 25  # Topic name must be shorter than this value


class TopicBase:
    """全てのTopicの基底クラス."""

    @classmethod
    def justify(cls):
        """Topic名の長さをTOPIC_LENGTHに揃えて返す.

        :return str:
        """
        return cls.__name__.ljust(TOPIC_LENGTH)

    @classmethod
    def text(cls, msg):
        """Topic名と引数を繋げて返す.

        特定のTopicに向けてメッセージを送る際に有用

        :param str msg: 送りたいメッセージ
        :return str:
        """
        return cls.justify() + msg

    @classmethod
    def json(cls, data):
        """Topic名と引数を繋げて返す.

        特定のTopicに向けてメッセージを送る際に有用

        :param dict data: JSONにして送りたいデータ
        :return str:
        """
        raise NotImplementedError


class WriteDB(TopicBase):
    """DBを扱うワーカーがsubscribeするTopic?."""

    pass
