:orphan:

サーバサイド
============

概観
----
:フレームワーク: Tornado_, Flask_ を採用
:コマンドラインインターフェース: Click_ を採用
:データベース処理: `MySQL Connector/Python`_, SQLAlchemy_, Alembic_ を採用

開発
  :テストフレームワーク: tox_, pytest_ を採用
  :静的コード解析: flake8_ を採用

.. _Tornado: http://www.tornadoweb.org/
.. _Flask: http://flask.pocoo.org/
.. _Click: http://click.pocoo.org/6/
.. _`MySQL Connector/Python`: https://dev.mysql.com/downloads/connector/python/
.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _Alembic: http://alembic.zzzcomputing.com/en/latest/
.. _tox: https://tox.readthedocs.io/
.. _pytest: http://pytest.org/latest/
.. _flake8: https://pypi.python.org/pypi/flake8

データモデル
------------
:Schema: メッセージスキーマ
:Module: モジュール
:MessageBox: メッセージボックス
:User: ユーザ
:Invitation: ユーザ招待リンク
:CcInfo: 自身や他CircleCoreの情報
:ReplicationLink: 共有リンク
:ReplicationMaster: 共有マスター
:ReplicationSlave: 共有リンクと参照中の他CircleCoreを結ぶ

ワーカー
--------
:DataReceiverWorker: メッセージを処理するワーカー。受信したメッセージをデータベースへ格納する。
:HTTPWorker: HTTP(Websocket)リクエストを処理するワーカー。メッセージレプリケーションのマスターとして働く。
:SlaveDriverWorker: HTTP(Websocket)リクエストを発行するワーカー。メッセージレプリケーションのスレーブとして働く。
