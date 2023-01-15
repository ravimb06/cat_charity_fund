from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)])
# В условиях задания лишь суперюзер может получить все донаты
# Обычный пользователь лишь свои
async def get_all_donations(
    sessions: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(sessions)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id', 'invested_amount', 'fully_invested',
                            'close_date'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получить список всех своих пожертвований."""
    donations = await donation_crud.get_by_user(
        session=session,
        user=user
    )
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={'user_id', 'invested_amount', 'fully_invested',
                            'close_date'},
    dependencies=[Depends(current_user)]
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Любой зарегистрированный пользователь может вносить пожертвования."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing_process(new_donation, CharityProject, session)
    await session.refresh(new_donation)
    return new_donation