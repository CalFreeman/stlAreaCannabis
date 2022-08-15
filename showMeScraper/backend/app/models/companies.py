from typing import Optional
from enum import Enum

from app.models.core import IDModelMixin, CoreModel

class CompanyBase(CoreModel):
    """
    All common characteristics of our Company resource
    """
    name: Optional[str]

class CompanyUpdate(CompanyBase):
    name: Optional[str]

class CompanyCreate(CompanyBase):
    name: str

class CompanyInDB(IDModelMixin, CompanyBase):
    name: str

class CompanyPublic(IDModelMixin, CompanyBase):
    pass

