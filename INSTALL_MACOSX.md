# Getting Starrted for Mac OS X
## 前提
- OS X El Capitan以降
- [Homebrew](http://brew.sh/index_ja.html) インストール済み

## 準備
### 各パッケージのインストール
- mysql
- nanomsg
- node
- pyenv

```
$ brew install mysql nanomsg node pyenv
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
$ git submodule init
$ git submodule update
```

### venv環境作成
```
$ virtualenv -p ~/.pyenv/versions/3.5.2/bin/python .env/3.5.2
$ . .env/3.5.2/bin/activate
(3.5.2) $ pip install -e git://github.com/nanomsg/nnpy.git#egg=nnpy
(3.5.2) $ pip install http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.2.2.tar.gz
(3.5.2) $ cd whisper && python setup.py install && cd ..
(3.5.2) $ pip install -e '.[test,mysql]'
```

### JavaScriptビルド
```
$ npm install
$ npm run build
```

### iniファイル設定
- [circle_core.ini.sample](/circle_core.ini.sample)をコピー、`circle_core.ini`にリネームし、内容を適宜修正する

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
1. http://127.0.0.1:8080 にアクセス
    - `circle_core.ini` の設定に従うため、変更している場合は適宜読み換える
1. `admin` / `admin` でログイン

## Botによるデータの取得
### Schema, MessageBox, Moduleを作成
1. Schemaを作成
```
(3.5.2) $ crcr schema add --name リアルタイム人流センサ speed:float lat:float lng:float direction:int x:float y:float timestamp:int pid:int psen:int
Schema "04c9520a-f50a-4314-bb46-aa8a2f3fbed1" is added. # 次で使用する
```

1. MessageBoxを作成
```
(3.5.2) $ crcr box add --schema 04c9520a-f50a-4314-bb46-aa8a2f3fbed1 --name 正常データ #UUIDは適宜変更
MessageBox "f34973b1-b5be-46a3-a8a8-f2bf306c3e70" is added. # 次で使用する
```

1. Moduleを作成
```
(3.5.2) $ crcr module add --name "リアルタイム人流センサ デバイス1" --box f34973b1-b5be-46a3-a8a8-f2bf306c3e70 #UUIDは適宜変更
Module "1a15b84b-99b5-4cd3-a509-6b72b68a86da" is added. # 次で使用する
```

### Databaseに反映
```
(3.5.2) $ crcr migrate
```

### サーバ起動
```
(3.5.2) $ crcr run --worker datareceiver
```

### BOT起動
```
(3.5.2) $ crcr bot echo --to ws://localhost:5000/module/1a15b84b-99b5-4cd3-a509-6b72b68a86da --box-id f34973b1-b5be-46a3-a8a8-f2bf306c3e70 # UUIDはModule, MessageBoxのものを使用
```

## レプリケーション
- `Botによるデータの取得` の手順で、Master環境でCircleCoreサーバを起動させておく
    - ModuleUUIDとIPAddresを控える

```
(3.5.2) $ crcr run --replicate 1a15b84b-99b5-4cd3-a509-6b72b68a86da@xxx.xxx.xxx.xxx:5000 # 控えたModuleUUID, MasterIPAddressを使用
```
