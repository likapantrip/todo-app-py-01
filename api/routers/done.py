from fastapi import APIRouter

# FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
router = APIRouter()


@router.put("/tasks/{task_id}/done", response_model=None)
async def mark_task_as_done(task_id: int):
    return


@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int):
    return