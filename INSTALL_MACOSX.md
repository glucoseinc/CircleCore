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
```

### venv環境作成
```
$ virtualenv -p ~/.pyenv/versions/3.5.2/bin/python .env/3.5.2
$ . .env/3.5.2/bin/activate
```

### インストール
```
(3.5.2) $ python setup.py develop
```

#### 手動でインストールする場合
```
(3.5.2) $ pip install -e git://github.com/nanomsg/nnpy.git#egg=nnpy
(3.5.2) $ pip install -e git://github.com/graphite-project/whisper.git@b783ab3f577f3f60db607adda241e29b7242bcf4#egg=whisper-0.10.0rc1
(3.5.2) $ pip install -e '.[test]'
```

### iniファイル設定
- [circle_core.ini.sample](/circle_core.ini.sample)をコピー、`circle_core.ini`にリネームし、内容を適宜修正する

### JavaScriptビルド
```
$ npm install
$ npm run build
```
- `circle_core.ini`の`[circle_core:http] skip_build`が`off`の場合、サーバ起動時に自動でビルドされる

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

1. Moduleを作成
```
(3.5.2) $ crcr module add --name "リアルタイム人流センサ デバイス1"
Module "1a15b84b-99b5-4cd3-a509-6b72b68a86da" is added. # 次で使用する
```

1. MessageBoxを作成
```
(3.5.2) $ crcr box add --schema 04c9520a-f50a-4314-bb46-aa8a2f3fbed1 --module 1a15b84b-99b5-4cd3-a509-6b72b68a86da --name 正常データ #UUIDは適宜変更
MessageBox "f34973b1-b5be-46a3-a8a8-f2bf306c3e70" is added. # 次で使用する
```

### BOT起動
```
(3.5.2) $ python sample/sensor_echo.py --box-id f34973b1-b5be-46a3-a8a8-f2bf306c3e70 # UUIDはMessageBoxのものを使用
```

## Setup SSL certificate
0. キーチェーンアクセス.appを起動
0. メニューバーのファイル -> 読み込む...をクリック
0. CircleCore/tests/tls.crtを選択
0. 検索窓にglucoseと入力、名前がglucoseの証明書を見つけてダブルクリック
0. ▶信頼を開いて常に信頼を選択

Chrome等だと自己証明している証明書には安全でない旨警告が出るが、それを無視すれば問題ない。
curlは問題なく通る。
