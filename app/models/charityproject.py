from sqlalchemy import (Column, DateTime, Integer, String, Text,
                        CheckConstraint, Boolean)

from app.core.db import Base


class CharityProject(Base):
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
    )

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
