from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import Donation
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.api.validators import (check_project_before_edit, 
                                check_charity_project_active,
                                check_name_duplicate,
                                check_charity_project_update)
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех проектов. Доступно всем пользователям"""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создание проектов доступно только Суперюзерам."""
    new_project = await charity_project_crud.create(project, session)
    await investing_process(new_project, Donation, session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Суперюзер может изменять название и описание
    существующего проекта,устанавливать для него новую требуемую сумму
    (но не меньше уже внесённой).
    """
    project = await check_project_before_edit(
        project_id, session
    )
    project = await check_charity_project_active(project, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_charity_project_update(
            project_id, session, obj_in.full_amount)
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session
    )
    project = await investing_process(project, Donation, session)
    return project


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удалить можно только проект в который не внесены средства.
    Доступно только Суперюзерам.
    """
    project = await check_project_before_edit(
        project_id, session
    )
    project = await charity_project_crud.remove(project, session)
    return project