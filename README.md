## 概要
FastAPIの学習を目的として作成したTODOアプリ。

### 主な機能
- TODO一覧取得
- TODO登録
- TODO更新
- TODO削除

### 技術スタック
- FastAPI
- Docker
- Poetry
- SQLAlchemy（予定）
- SQLite（予定）

### 参考書籍
[FastAPI入門](https://zenn.dev/sh0nk/books/537bb028709ab9)

## ディレクトリ構成
```
todo-app-py-01
├─ /.dockervenv        # Docker コンテナ用の仮想環境
├─ /.venv              # ローカル環境の仮想環境
├─ api
│   ├─ __init__.py
│   ├─ main.py
│   └─ routers
│       ├─ __init__.py
│       ├─ done.py
│       └─ task.py
├─ .gitattributes
├─ .gitignore
├─ docker-compose.yaml
├─ Dockerfile
├─ poetry.lock
├─ pyproject.toml
└─ README.md
```

## 手順
### Docker環境を構築
1. DockerがPCにインストールされていることを確認する
    ```bash
    $ docker compose version
    # Docker Compose version v5.1.3
    ```
1. プロジェクトディレクトリの直下に`docker-compose.yaml`と`Dockerfile`を作成する
1. 下記コマンドを実行することで、Dockerイメージをビルドする
    ```bash
    $ docker compose build
    # [+] build 1/1
    #  ✔ Image todo-app-py-01-demo-app Built                                    111.4s
    ```
1. `pyproject.toml`を作成する
    1. 下記コマンドを実行することで、Dockerコンテナ（demo-app）の中で、 `poetry init` コマンドを実行する
        ```bash
        $ docker compose run \
        --entrypoint "poetry init \
            --name demo-app \
            --dependency fastapi \
            --dependency uvicorn[standard]" \
        demo-app
        ```
    1. Authorのパートのみ `n` を入力し、それ以外はすべてEnterキーを押下する
        ```bash
        Version [0.1.0]:  
        Description []:  
        Author [None, n to skip]:  n
        License []:  
        Compatible Python versions [>=3.11]:  
        ...
        ```
1. 下記コマンドを実行し、`pyproject.toml` に定義された依存パッケージ（FastAPI、uvicorn）をインストールする
    ```bash
    $ docker compose run --entrypoint "poetry install --no-root" demo-app
    ```
1. インストール完了後、`poetry.lock` がプロジェクトディレクトリ直下に作成されたことを確認する

### FastAPIを実行
1. プロジェクトディレクトリの直下に `api` ディレクトリを作成する
1. `api/__init__.py`と `api/main.py`を作成する
1. 下記コマンドを実行し、サーバーを立ち上げる
    ```bash
    $ docker compose up
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. `Execute` をクリックし、`{"message": "hello world!"}`が返ることを確認する
    [![Image from Gyazo](https://i.gyazo.com/11201b29b3a86068cd5724ddda310268.gif)](https://gyazo.com/11201b29b3a86068cd5724ddda310268)

### ルーター実装
1. apiディレクトリに `__init__.py` と `task.py` と `done.py` を作成する
1. `main.py` を編集する
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. ６つのパスオペレーション関数に対応するエンドポイントが表示されることを確認する
    [![Image from Gyazo](https://i.gyazo.com/bf9e9aab6fd65a27e127c7783e3f574a.png)](https://gyazo.com/bf9e9aab6fd65a27e127c7783e3f574a)

## 補足説明
### Docker関連ファイル
|ファイル名|役割|
|-|-|
|docker-compose.yaml|Docker Composeの設定ファイル。コンテナの構成（イメージ、ポート、ボリュームなど）を定義する。`build` を指定した場合は `Dockerfile` を利用してイメージを作成する。|
|Dockerfile|Dockerイメージの設計図。Python環境の作成やライブラリのインストール手順を定義する。|

### Docker構成
#### ファイル構成・volume同期
```
ホスト(Mac)
todo-app-py-01 (プロジェクトフォルダ)  <────────────────────────────────────────────────────────────────┐
│                                                                                                    │ /src と同期
├─ /.venv                                                                                            │ (設定: volumes の .:/src)
├─ docker-compose.yaml                                                                               │
├─ Dockerfile                                                                                        │
├─ poetry.lock                                                                                       │
├─ pyproject.toml                                                                                    │
│                                                                                                    │
└─ /.dockervenv                     <────────────────────┐                                           │
                                                         │ /src/.venv と同期                          │
                                                         │ (設定: volumes の .dockervenv:/src/.venv)  │
Dockerコンテナ (demo-app)                                 │                                           │
│                                                        │                                           │
├─ /src/.venv                       <────────────────────┘                                           │
│                                                                                                    │
└─ /src                             <────────────────────────────────────────────────────────────────┘
    ├─ api
    │    ├─ __init__.py
    │    └─ main.py        <- FastAPIアプリを定義
    ├─ docker-compose.yaml
    ├─ Dockerfile
    └─ pyproject.toml
```

- volumes はホストとコンテナでファイルを同期する仕組み
- コードを修正すると volumes によりコンテナ側にも即時反映される

#### ネットワーク通信
```
ブラウザ
    │
    ▼
http://localhost:8000
    │ 通信
    │ (設定: ports)
    ▼
Dockerコンテナ(demo-app)
    │
    ▼
uvicorn
    │
    ▼
FastAPI(api/main.py)
```

- ports はホストとコンテナで通信する仕組み
- FastAPIはコンテナ内で動作する

### `poetry init` コマンド
`pyproject.toml` を生成し、FastAPI本体とASGIサーバーである `uvicorn` を依存関係として登録する。

## Router構成
1ファイルに全てのパスオペレーション関数を定義すると、可読性などが低下する。
そのため、リソースごとにファイルを分ける。

今回のケースだと、`/tasks` と `/tasks/{task_id}/done` の2つに大別できる。
