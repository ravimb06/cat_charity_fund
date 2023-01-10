from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    user_id: Optional[int] = Field(None)
    comment: Optional[str] = Field(None)
    full_amount: PositiveInt = Field(...,)
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    create_date: datetime = datetime.now()
    close_date: datetime = Field(None)

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int

    class Config:
        orm_mode = True
