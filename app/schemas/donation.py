from typing import Optional

from pydantic import BaseModel, Field, validator

class DonationBase(BaseModel):
    