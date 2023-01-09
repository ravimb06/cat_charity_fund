from fastapi import APIRouter

from app.api.endpoints import charity_project_router
main_router = APIRouter()
main_router.include_router(
    charity_project_router, prefix='/charity_project', tags=['Charity Projects']
)