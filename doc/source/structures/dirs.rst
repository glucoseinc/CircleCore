:orphan:

ディレクトリ構成
================

::

    CircleCore
    ├── circle_core
    │   ├── alembic
    │   │   └── versions
    │   ├── cli
    │   ├── core
    │   ├── helpers
    │   ├── models
    │   ├── web
    │   │   ├── api
    │   │   ├── authorize
    │   │   ├── download
    │   │   ├── public
    │   │   ├── src
    │   │   │   ├── css
    │   │   │   ├── images
    │   │   │   └── js
    │   │   │       ├── actions
    │   │   │       ├── components
    │   │   │       ├── containers
    │   │   │       ├── models
    │   │   │       ├── public
    │   │   │       ├── reducers
    │   │   │       ├── routes
    │   │   │       ├── sagas
    │   │   │       └── store
    │   │   └── templates
    │   └── workers
    │       ├── http
    │       └── slave_driver
    ├── doc
    │   └── source
    │       ├── _static
    │       └── apis
    ├── sample
    └── tests

circle_core
-----------
CircleCoreのソースコード。

alembic
-------
Alembic_ に関連するファイル群。

.. _Alembic: http://alembic.zzzcomputing.com/en/latest/

versions
  metadataデータベースのスキーマを更新する際の version_ ファイルを格納。

.. _version: http://alembic.zzzcomputing.com/en/latest/tutorial.html

cli
---
`crcr` コマンドを構成。

core
----
CircleCoreのコア部分。

helpers
-------
ヘルパークラス/関数群。

models
------
metadataデータベースのデータモデル。

web
---
WebUIを構成。

api
  API群。

authorize
  ユーザー認証に関連する。

download
  ダウンロードAPI群。

public
  認証を要しない箇所を格納。

src
  クライアントサイドを構成。

  css
    cssファイルを格納。

  images
    画像ファイルを格納。

  js_
    クライアントサイドのスクリプトを構成。

templates
  サーバサイドのHTMLファイルテンプレート。

workers
-------
CircleCoreのワーカープロセス。

----

.. _js:

js
--
クライアントサイドのスクリプトを構成。

actions
  `Redux Action`_ を格納。

.. _`Redux Action`: http://redux.js.org/docs/basics/Actions.html

components
  `React Component`_ を格納。

.. _`React Component`: https://facebook.github.io/react/docs/react-component.html

containers
  `Redux Container`_ を格納。

.. _`Redux Container`: http://redux.js.org/docs/basics/UsageWithReact.html

models
  metadataデータベースのデータモデル。

public
  認証を要しない箇所を格納。

reducers
  `Redux Reducer`_ を格納。

.. _`Redux Reducer`: http://redux.js.org/docs/basics/Reducers.html

routes
  `React Router`_ を格納。

.. _`React Router`: https://github.com/ReactTraining/react-router

sagas
  `Redux Saga`_ を格納。

.. _`Redux Saga`: https://redux-saga.github.io/redux-saga/

store
  `Redux Store`_ を格納。

.. _`Redux Store`: http://redux.js.org/docs/basics/Store.html

doc
---
本ドキュメントを構成。

sample
------
CircleCoreに外部から接続する時のサンプルスクリプト群。

tests
-----
CircleCore Test。
