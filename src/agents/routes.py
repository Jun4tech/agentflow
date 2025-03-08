from fastapi import APIRouter

router = APIRouter(prefix="/api")

@router.get("/")
async def test_api():
    return {"message": "Hello World"}

