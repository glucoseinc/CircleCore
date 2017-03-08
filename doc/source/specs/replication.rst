:orphan:

===========
同期の仕様
===========

用語
===========


Master
  データの送り手

Slave
  データの受け取り手

共有リンク
  Master側が開く、Slaveにデータを送るためのWebsocketエンドポイント

共有マスター
  Slave側からみたMasterの事


同期フロー
===========

同期のフローは以下の通り::

  participant Master as M
  participant Slave as S
  Note left of M: "HANDSHAKING" state
  S->M: "hello" cmd
  Note left of M: "MIGRATING" state
  M->S: "migrate" cmd
  S->M: "migrated" cmd
  Note left of M: "SYNCING" state
  M->S: "sync_message" cmds...
  M->S: "new_message" cmds...
  Note right of S: when Slave's circle core info is updated
  S->M: "circle_core_updated" cmd

.. image:: ./replication-flow.svg


同期ステータス
==============

Master, Slaveはそれぞれ `HANDSHAKING` ,  `MIGRATING` ,  `SYNCING` のステータスを持つ


----------------
`HANDSHAKING`
----------------

to be describe...

"hello" コマンド
---------------------

to be describe...


----------------
`MIGRATING`
----------------

to be describe...

"migrate" コマンド
---------------------

to be describe...

"migrated" コマンド
---------------------

to be describe...


----------------
`SYNCING`
----------------

to be describe...


"sync_message" コマンド
-----------------------

to be describe...


"new_message" コマンド
----------------------

to be describe...
