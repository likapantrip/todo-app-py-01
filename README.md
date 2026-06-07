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

## 補足説明
### Docker関連ファイル
|ファイル名|役割|
|-|-|
|docker-compose.yaml|Docker Composeの設定ファイル。コンテナの構成（イメージ、ポート、ボリュームなど）を定義する。`build` を指定した場合は `Dockerfile` を利用してイメージを作成する。|
|Dockerfile|Dockerイメージの設計図。Python環境の作成やライブラリのインストール手順を定義する。|

### Docker構成
```
ホスト(Mac)
todo-app-py-01 (プロジェクトフォルダ)  <────────────────────────────────────────────────────────────────┐
│                                                                                                    | /src と同期
├─ /.venv                                                                                            | (設定: volumes の .:/src)
├─ docker-compose.yaml                                                                               |
├─ Dockerfile                                                                                        |
├─ poetry.lock                                                                                       |
├─ pyproject.toml                                                                                    |
│                                                                                                    |
├─ /.dockervenv                     <────────────────────┐                                           |
│                                                        | /src/.venv と同期                          |
│                                                        | (設定: volumes の .dockervenv:/src/.venv)  |
└─ localhost:8000                   ─────┐               |                                           |
                                         | 通信           |                                           |
                                         | (設定: ports)  |                                           |
Dockerコンテナ (demo-app)                 |               |                                           |
│                                        |               |                                           |
├─ FastAPIプロセス(後続で実装予定)      <────┘               |                                           |
│   └─ 8000番ポートで待ち受け                               |                                           |
│                                                        |                                           |
├─ /src/.venv                       <────────────────────┘                                           |
│                                                                                                    |
└─ /src                             <────────────────────────────────────────────────────────────────┘
    ├─ app  ※ FastAPIの実体は、/src/appのコード (appディレクトリは後続で作成)
    ├─ docker-compose.yaml
    ├─ Dockerfile
    └─ pyproject.toml
```

- volumes はホストとコンテナでファイルを同期する仕組み
- ports はホストとコンテナで通信する仕組み
- FastAPIはコンテナ内で動作する
- コードを修正すると volumes によりコンテナ側にも即時反映される

### `poetry init` コマンド
`pyproject.toml` を生成し、FastAPI本体とASGIサーバーである `uvicorn` を依存関係として登録する。
