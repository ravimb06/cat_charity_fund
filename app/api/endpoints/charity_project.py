from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.api.validators import check_project_before_edit

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


@router.patch('/{project_id}', response_model=CharityProjectDB)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_before_edit(
        project_id, session
    )
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session
    )
    return project


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_before_edit(
        project_id, session
    )
    project = await charity_project_crud.remove(project, session)
    return project