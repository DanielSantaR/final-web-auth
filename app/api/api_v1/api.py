from fastapi import APIRouter

from app.api.api_v1.endpoints import login, root

api_router = APIRouter()
api_router.include_router(root.router)
api_router.include_router(login.router, tags=["login"])
