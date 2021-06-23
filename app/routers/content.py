from fastapi import APIRouter

router = APIRouter(
    prefix="/api/content",
    tags=["content"]
)


@router.get("/list")
async def get_list():
    return {"message": "content list."}


# @router.post("/register")
