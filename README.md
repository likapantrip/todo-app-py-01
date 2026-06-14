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
│   ├─ routers
│   │   ├─ __init__.py
│   │   ├─ done.py
│   │   └─ task.py
│   └─ schemas
│       ├─ __init__.py
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
1. プロジェクトディレクトリの直下に `docker-compose.yaml` を作成する
    ```docker-compose.yaml
    services:                      # 起動するコンテナの一覧を定義
    demo-app:                    # サービス名(コンテナを識別する名前)
        build: .                   # カレントディレクトリのDockerfileを使ってイメージを作成 (.は、カレントディレクトリ)
        volumes:                   # ホスト(PC)とコンテナの間でファイルを共有(同期)する設定
        - .dockervenv:/src/.venv # ホストマシンの .dockervenv を、コンテナ内の /src/.venv と同期
        - .:/src                 # ホストマシンのカレントディレクトリ全体をコンテナの /src と同期
        ports:                     # ホストマシンとコンテナの間でポートを接続するための設定
        - 8000:8000              # localhost:8000 へのアクセスを、コンテナの8000番ポートへ転送
    ```
1. プロジェクトディレクトリの直下に `Dockerfile` を作成する
    ```Dockerfile
    # Python3.11が使えるLinux環境をベースイメージとして指定
    FROM python:3.11-slim

    # Pythonのログを即座に表示する環境変数を設定
    ENV PYTHONUNBUFFERED=1 

    # 作業ディレクトリを指定
    WORKDIR /src

    # pipを使ってpoetryをインストール
    RUN pip install poetry

    # poetryの定義ファイル(pyproject.toml / poetry.lock)をコピー
    # 存在するファイルのみコピー
    COPY pyproject.toml* poetry.lock* ./

    # 仮想環境をプロジェクト内(.venv)に作成するように、poetryを設定変更
    RUN poetry config virtualenvs.in-project true

    # (pyproject.tomlが存在する場合、)poetryで依存ライブラリをインストール
    # --no-rootオプションは、プロジェクトのルートパッケージをインストールしないようにするためのもの
    RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

    # uvicornのサーバーを立ち上げ、FastAPIのアプリを起動
    ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]
    ```
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
1. `api/__init__.py` を作成する
1. `api/main.py`を作成する
    ```py:main.py
    from fastapi import FastAPI

    # FastAPIのインスタンスを作成。uvicornからこのappが読み込まれ、リクエストを処理する。
    app = FastAPI()

    # GET /hello にアクセスされたときに実行される処理を定義
    @app.get("/hello")
    async def hello():
        return {"message": "hello world!"}
    ```
1. 下記コマンドを実行し、サーバーを立ち上げる
    ```bash
    $ docker compose up
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. `Execute` をクリックし、`{"message": "hello world!"}`が返ることを確認する
    [![Image from Gyazo](https://i.gyazo.com/11201b29b3a86068cd5724ddda310268.gif)](https://gyazo.com/11201b29b3a86068cd5724ddda310268)

### ルーター実装
1. apiディレクトリに `router/__init__.py` を作成する
1. apiディレクトリに `router/task.py` を作成する
    ```py:task.py
    from fastapi import APIRouter

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()


    @router.get("/tasks")
    async def list_tasks():
        pass # 何もしない文


    @router.post("/tasks")
    async def create_task():
        pass # 何もしない文


    @router.put("/tasks/{task_id}")
    async def update_task():
        pass # 何もしない文


    @router.delete("/tasks/{task_id}")
    async def delete_task():
        pass # 何もしない文
    ```
1. apiディレクトリに `router/done.py` を作成する
    ```py:done.py
    from fastapi import APIRouter

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()


    @router.put("/tasks/{task_id}/done")
    async def mark_task_as_done():
        pass # 何もしない文


    @router.delete("/tasks/{task_id}/done")
    async def unmark_task_as_done():
        pass # 何もしない文
    ```
1. `main.py` を編集する
    ```py:main.py
    from fastapi import FastAPI
    from api.routers import task, done

    # FastAPIのインスタンスを作成。uvicornからこのappが読み込まれ、リクエストを処理する。
    app = FastAPI()

    # FastAPI本体にルーターを登録する。これにより、ルーターで定義されたエンドポイントが有効になる。
    # この登録がない場合、Swagger UIなどでエンドポイントが表示されない。
    app.include_router(task.router)
    app.include_router(done.router)
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. ６つのパスオペレーション関数に対応するエンドポイントが表示されることを確認する
    [![Image from Gyazo](https://i.gyazo.com/bf9e9aab6fd65a27e127c7783e3f574a.png)](https://gyazo.com/bf9e9aab6fd65a27e127c7783e3f574a)
1. Response bodyは `null` になることを確認する
    [![Image from Gyazo](https://i.gyazo.com/ca898b52ab9264a52c95f0d5e9325e39.png)](https://gyazo.com/ca898b52ab9264a52c95f0d5e9325e39)

### スキーマ実装
1. apiディレクトリに `schemas/__init__.py` を作成する
1. apiディレクトリに `schemas/task.py` を作成する
    ```py:task.py
    from typing import Optional

    from pydantic import BaseModel, Field

    # タスクのスキーマ定義(APIの入出力に使用)
    class Task(BaseModel):
        id: int
        title: Optional[str] = Field(None, example="クリーニングを取りに行く")
        done: bool = Field(False, description="完了フラグ")
    ```
1. `router/task.py`を編集する
    ```py:task.py
    from fastapi import APIRouter
    from typing import List

    import api.schemas.task as task_schema

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()


    @router.get("/tasks", response_model=List[task_schema.Task])
    async def list_tasks():
        return [task_schema.Task(id=1, title="1つ目のTODOタスク")]


    @router.post("/tasks")
    async def create_task():
        pass # 何もしない文


    @router.put("/tasks/{task_id}")
    async def update_task():
        pass # 何もしない文


    @router.delete("/tasks/{task_id}")
    async def delete_task():
        pass # 何もしない文
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. Response bodyが追加されたことを確認する
    [![Image from Gyazo](https://i.gyazo.com/46e6d7c197a91d244131e915d40df5cb.png)](https://gyazo.com/46e6d7c197a91d244131e915d40df5cb)
1. `schemas/task.py` を編集する
    ```py:task.py
    from typing import Optional

    from pydantic import BaseModel, Field

    class TaskBase(BaseModel):
        title: Optional[str] = Field(None, example="クリーニングを取りに行く")

    class TaskCreate(TaskBase):
        pass # 何もしない文

    class Task(TaskBase):
        id: int
        done: bool = Field(False, description="完了フラグ")

        class Config:
            orm_mode = True

    class TaskCreateResponse(TaskCreate):
        id: int

        class Config:
            orm_mode = True
    ```
1. `routers/task.py` を編集する
    ```py:task.py
    from fastapi import APIRouter
    from typing import List

    import api.schemas.task as task_schema

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()


    @router.get("/tasks", response_model=List[task_schema.Task])
    async def list_tasks():
        return [task_schema.Task(id=1, title="1つ目のTODOタスク")]


    @router.post("/tasks", response_model=task_schema.TaskCreateResponse)
    async def create_task(task_body: task_schema.TaskCreate):
        return task_schema.TaskCreateResponse(id=1, **task_body.dict())


    @router.put("/tasks/{task_id}")
    async def update_task():
        pass # 何もしない文


    @router.delete("/tasks/{task_id}")
    async def delete_task():
        pass # 何もしない文
    ```
1. ブラウザで[http://localhost:8000/docs](http://localhost:8000/docs)にアクセスする
1. POSTのリクエストボディが動的に変更されることを確認する
    [![Image from Gyazo](https://i.gyazo.com/38c6eb1af4967121eacfc8e266d96566.gif)](https://gyazo.com/38c6eb1af4967121eacfc8e266d96566)
1. `routers/task.py` を編集する
    ```py:task.py
    from fastapi import APIRouter
    from typing import List

    import api.schemas.task as task_schema

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()


    @router.get("/tasks", response_model=List[task_schema.Task])
    async def list_tasks():
        return [task_schema.Task(id=1, title="1つ目のTODOタスク")]


    @router.post("/tasks", response_model=task_schema.TaskCreateResponse)
    async def create_task(task_body: task_schema.TaskCreate):
        return task_schema.TaskCreateResponse(id=1, **task_body.dict())


    @router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
    async def update_task(task_id: int, task_body: task_schema.TaskCreate):
        return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())


    @router.delete("/tasks/{task_id}", response_model=None)
    async def delete_task(task_id: int):
        return
    ```
1. `routers/done.py` を編集する
    ```py:done.py
    from fastapi import APIRouter

    # FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
    router = APIRouter()


    @router.put("/tasks/{task_id}/done", response_model=None)
    async def mark_task_as_done(task_id: int):
        return


    @router.delete("/tasks/{task_id}/done", response_model=None)
    async def unmark_task_as_done(task_id: int):
        return
    ```

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
