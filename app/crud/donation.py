from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    pass


charity_project_crud = CRUDDonation(Donation)