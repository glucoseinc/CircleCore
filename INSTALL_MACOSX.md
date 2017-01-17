# Getting Starrted for Mac OS X
## 前提
- OS X El Capitan以降
- [Homebrew](http://brew.sh/index_ja.html) インストール済み

## 準備
### 各パッケージのインストール
- redis
- mysql
- nanomsg
- node
- pyenv

```
$ brew install redis mysql nanomsg node pyenv
```

- 各パッケージの初期設定を行う
    - `brew install` 時のメッセージ、各パッケージのDocs等を参照

### MySQLにDatabase作成
```
$ mysql -u root
mysql> CREATE DATABASE crcr;
```

### python3.5.2インストール
```
$ pyenv install 3.5.2
```

### virtualenvインストール
```
$ pip install virtualenv
```
- Global環境にインストールされる

## CircleCoreの準備
### 最新ソース取得
```
$ git clone git@github.com:glucoseinc/CircleCore.git  # SSH接続時
$ cd CircleCore
$ git checkout master
$ git pull
```

### venv環境作成
```
$ virtualenv -p ~/.pyenv/versions/3.5.2/bin/python .env/3.5.2
$ . .env/3.5.2/bin/activate
(3.5.2) $ pip install -e git://github.com/nanomsg/nnpy.git#egg=nnpy
(3.5.2) $ pip install http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.2.1.tar.gz
(3.5.2) $ pip install -e '.[test,redis,mysql]'
```

### 環境変数設定
```
(3.5.2) $ export CRCR_METADATA=redis://localhost:6379/0   # portは必要に応じて変更
(3.5.2) $ export CRCR_UUID=$(uuidgen)
(3.5.2) $ export CRCR_DATABASE=mysql+mysqlconnector://root@localhost/crcr
```

### JavaScriptビルド
```
$ npm install
$ npm run build
```

## サーバ起動
```
(3.5.2) $ crcr run
```

## ユーザ作成
```
(3.5.2) $ crcr user add --account admin --password admin --admin
(3.5.2) $ crcr user add --account user --password user
```

## 確認
1. http://localhost:5000 にアクセス
1. `admin` / `admin` でログイン
