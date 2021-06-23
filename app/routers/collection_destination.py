from fastapi import APIRouter

router = APIRouter(
    prefix="/api/collection_destination",
    tags=["collection_destination"]
)


@router.get("/list")
async def get_list():
    return {"message": "collection_destination list."}


# @router.post("/register")
