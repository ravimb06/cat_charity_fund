from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: PositiveInt = Field(...,)
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    create_date: datetime = datetime.now()
    close_date: datetime = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectCreate):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int

    class Config:
        orm_mode = True
