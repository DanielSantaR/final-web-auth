from fastapi import APIRouter

from app.api.api_v1.endpoints import employee, login, root, vehicle

api_router = APIRouter()
api_router.include_router(root.router)
api_router.include_router(login.router, tags=["login"])
api_router.include_router(employee.router, prefix="/employees", tags=["employee"])
api_router.include_router(vehicle.router, prefix="/vehicles", tags=["vehicle"])
