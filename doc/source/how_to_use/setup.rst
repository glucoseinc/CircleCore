:orphan:

使い方
==============================


---------------------------
起動方法
---------------------------


Dockerを使う場合
---------------------------


Dockerコマンドよりビルドと実行を行う。::

	% docker build -t circle_core .
	% docker run -it circle_core


以下のコマンドで、CLIツールが使える。::

	% docker exec -it [CONTAINER ID] crcr


マシン上で直接立ち上げる
---------------------------

`README <https://github.com/glucoseinc/CircleCore/blob/master/README.md>`を参照。



---------------------------
管理者ユーザーを作成する
---------------------------

CLIツールから行う。
起動方法によってCLIツールの使い方が違うことに注意。::

	% crcr user add --admin --account admin --password [管理者のパスワード]



---------------------------
Web管理画面に接続する
---------------------------

CircleCoreの起動ログにWeb管理画面のURLが記載されているので、そこに接続する。
管理者のアカウントでログインする。


:doc:`invite`

:doc:`scheme`

:doc:`module`
