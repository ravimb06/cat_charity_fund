from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_project = await charity_project_crud.create(project, session)
    return new_project