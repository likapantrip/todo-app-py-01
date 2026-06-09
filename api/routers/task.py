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