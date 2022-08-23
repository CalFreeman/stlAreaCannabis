import string
from typing import Optional
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel

class DispensaryBase(CoreModel):
    """
    Leaving off company_id_ and _ from base model
    """
    flower_url: Optional[str]
    pre_rolls_url: Optional[str]
    vaporizers_url: Optional[str]
    concentrates_url: Optional[str]
    edibles_url: Optional[str]
    tinctures_url: Optional[str]
    topicals_url: Optional[str]
    cbd_url: Optional[str]
    address: Optional[str]

class DispensaryUpdate(DispensaryBase):
    pass

class DispensaryCreate(DispensaryBase):
    company_id: int

class DispensaryInDB(IDModelMixin, DateTimeModelMixin, DispensaryBase):
    company_id: int


class DispensaryPublic(IDModelMixin, DateTimeModelMixin, DispensaryBase):
    pass

