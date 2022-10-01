from enum import Enum
from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from pydantic import Json, HttpUrl
from typing import Any, Dict, AnyStr, List, Union, Optional
from fastapi import FastAPI


class RawJsonBase(CoreModel):
    """
    Leaving off company_id_ and _ from base model
    """
    json_doc: Optional[str]


class RawJsonUpdate(RawJsonBase):
    pass

class RawJsonCreate(RawJsonBase):
    """
    The only field required to create a raw_json
    """
    json_doc: Optional[str]


class RawJsonInDB(IDModelMixin, RawJsonBase):
    pass

class RawJsonPublic(IDModelMixin, RawJsonBase):
    pass

