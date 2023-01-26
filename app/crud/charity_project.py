from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_id(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Получить проект по ID."""
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        db_project = db_project.scalars().first()
        return db_project

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить ID проекта по названию."""
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name)
        )
        project_id = project_id.scalars().first()
        return project_id

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[dict]:
        projects = await session.execute(
            select([CharityProject.name,
                    CharityProject.create_date,
                    CharityProject.close_date,
                    CharityProject.description]).where(
                CharityProject.fully_invested
            ).order_by((func.julianday(CharityProject.close_date) -
                        func.julianday(CharityProject.create_date)).desc())
        )
        projects = projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)