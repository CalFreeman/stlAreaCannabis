from typing import Optional
from enum import Enum
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from pydantic import Json, HttpUrl

class RawJsonBase(CoreModel):
    """
    Leaving off company_id_ and _ from base model
    """
    json_doc: str

class RawJsonUpdate(RawJsonBase):
    pass

class RawJsonCreate(RawJsonBase):
    """
    The only field required to create a raw_json
    """
    json_doc: str

class RawJsonInDB(IDModelMixin, RawJsonBase):
    pass

class RawJsonPublic(IDModelMixin, RawJsonBase):
    pass

