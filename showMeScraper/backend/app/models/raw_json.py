from typing import Optional
from enum import Enum
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from pydantic import Json, HttpUrl

class RawJsonBase(CoreModel):
    """
    Leaving off company_id_ and _ from base model
    """
    json_doc: Json

class RawJsonUpdate(RawJsonBase):
    pass

class RawJsonCreate(RawJsonBase):
    """
    The only field required to create a raw_json
    """
    pass

class RawJsonInDB(IDModelMixin, DateTimeModelMixin, RawJsonBase):
    pass

class RawJsonPublic(IDModelMixin, DateTimeModelMixin, RawJsonBase):
    pass

