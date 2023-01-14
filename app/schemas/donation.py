from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None)
    full_amount: PositiveInt = Field(...,)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    user_id: Optional[int] = Field(None)
    comment: Optional[str] = Field(None)
    full_amount: PositiveInt = Field(...,)
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = Field(False, example=True)
    create_date: datetime = datetime.now().isoformat('T', 'seconds')
    close_date: datetime = Field(
        None, example=datetime.now().isoformat('T', 'seconds')
    )

    class Config:
        orm_mode = True
