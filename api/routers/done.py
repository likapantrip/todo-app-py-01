from fastapi import APIRouter

# FastAPIでAPIのルーティング（URLと処理の対応付け）をまとめるためのオブジェクトを作成する。
router = APIRouter()


@router.put("/tasks/{task_id}/done")
async def mark_task_as_done():
    pass # 何もしない文


@router.delete("/tasks/{task_id}/done")
async def unmark_task_as_done():
    pass # 何もしない文