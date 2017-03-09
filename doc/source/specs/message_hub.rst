:orphan:

メッセージハブの仕様
======================


CircleCoreはnanomsgを使って、メッセージを作成、流通させるハブを持っている。ここではそのハブの仕様、使い方について解説する。

------------
ハブ
------------

CircleCore内では、Requestハブ、Pub/Subハブの2種類のハブを持つ。それぞれの役割は以下の通り。


Requestハブ
  クライアントからCircleCoreに対する要求を受け付ける
Pub/Subハブ
  CirlceCore内に届いたメッセージ、メタデータの更新についての情報が通知される


.. note::

  何故か？
  nanomsgの仕様で、Pub/SubのTopologyを構成する場合、Subが複数ある場合はPubは1socketしか開けない。
  その為、別にRequestハブを持ち、クライアントからの要求に答える必要がある。


-----------------
Requestプロトコル
-----------------


新しくメッセージを登録する
----------------------------


リクエスト
  `new_message`
フォーマット
  .. code-block:: javascript

      {
        "request": "new_message",
        "payload": {...}, /* object メッセージのデータ*/
        "box_id": "e7f03b36-4320-4612-828e-154e152845da"  /* MessageBoxのUUID */
      }




-----------------
Pub/Subプロトコル
-----------------

Topic長: 64chars


新着メッセージ
-----------------

トピック
  `module:[b58encoded Module UUID]:[b58encoded MessageBox UUID]`
フォーマット
  .. code-block:: javascript

      {
        "timestamp": "1486621655.249531", /* str メッセージを受け付け付けたタイミングでのunix epoch */
        "counter": 238, /* int メッセージを受け付けたタイミングでのカウンタ */
        "payload": {...} /* object メッセージのデータ */
      }


スキーマのメタデータ更新
---------------------------

to be describe...


モジュールのメタデータ更新
---------------------------

to be describe...


メッセージボックスのメタデータ更新
----------------------------------

to be describe...
