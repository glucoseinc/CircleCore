:orphan:

クライアントサイド
==================

概観
----
:フレームワーク: React_ + Redux_ を採用
:ルーティング: `React Router`_ を採用
:非同期処理: redux-saga_ を採用
:API処理: superagent_ を採用
:データモデル: Immutable_ を採用
:データ管理: normalizr_ を採用
:`Material Design`_: Material-UI_ を採用
:データ視覚化: Rickshaw_ を採用

開発
  :JavaScriptコンパイラ: Babel_ を採用
  :静的コード解析: ESLint_ を採用
  :css変換: PostCSS_ を採用
  :モジュールバンドラ: webpack_ を採用

.. _React: https://facebook.github.io/react/
.. _Redux: http://redux.js.org/
.. _`React Router`: https://github.com/ReactTraining/react-router
.. _redux-saga: https://redux-saga.github.io/redux-saga/
.. _superagent: http://visionmedia.github.io/superagent/
.. _Immutable: https://facebook.github.io/immutable-js/
.. _normalizr: https://github.com/paularmstrong/normalizr
.. _`Material Design`: https://material.io/
.. _Material-UI: http://www.material-ui.com/
.. _Rickshaw: http://code.shutterstock.com/rickshaw/

.. _Babel: https://babeljs.io/
.. _ESLint: http://eslint.org/
.. _PostCSS: http://postcss.org/
.. _webpack: https://webpack.js.org/


Redux
-----
State_ / Reducer_
  :asyncs: 非同期処理の処理実行中状態
  :auth: ユーザ認証トークン
  :entities: サーバから取得したデータを格納
  :error: サーバから通知されたエラー情報を格納
  :page: 画面表示に関する状態
  :misc: 上記に該当しない、その他の状態

Action_
  :auth: ユーザ認証
  :error: エラー処理に関する操作
  :page: 画面表示に関する操作
  :データ操作:
            - ccInfo
            - invitation
            - module
            - replicationLink
            - replicationMaster
            - schema
            - schemaPropertyType
            - user

.. _State: http://redux.js.org/docs/Glossary.html#state
.. _Action: http://redux.js.org/docs/Glossary.html#action
.. _Reducer: http://redux.js.org/docs/Glossary.html#reducer

redux-saga_
  :async: データ操作のリクエストを受け付け、成功/失敗アクションを発行する。
  :auth: 画面遷移時のトークンの更新を行う。
  :error: データ操作リクエストの失敗アクションを受け付け、エラー表示アクションを発行する。
  :location: データ作成/削除リクエストの成功アクションなど、特定のアクションを受け付け、画面遷移アクションを発行する。
  :snackbar: データ操作リクエストの成功アクションを受け付け、スナックバー表示アクションを発行する。
