from typing import List
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.raw_json import RawJsonCreate, RawJsonUpdate, RawJsonInDB

CREATE_RAW_JSON_QUERY = """
    INSERT INTO raw_json (json_doc)
    VALUES (:json_doc)
    RETURNING id, json_doc;
"""
GET_RAW_JSON_BY_ID_QUERY = """
    SELECT id, json_doc
    FROM raw_json
    WHERE id = :id;
"""

GET_ALL_RAW_JSON_QUERY = """
    SELECT id, json_doc
    FROM raw_json;
"""

UPDATE_RAW_JSON_BY_ID_QUERY = """
    UPDATE raw_json
    SET json_doc = :json_doc
    WHERE id = :id
    RETURNING id, json_doc;
"""

DELETE_RAW_JSON_BY_ID_QUERY = """
    DELETE FROM raw_json
    WHERE id = :id
    RETURNING id;
""" 

class RawJsonRepository(BaseRepository):
    """"
    All database actions associated with the raw_json resource
    """
    async def create_raw_json(self, *, new_raw_json: RawJsonCreate) -> RawJsonInDB:
        query_values = new_raw_json.dict()
        raw_json = await self.db.fetch_one(query=CREATE_RAW_JSON_QUERY, values=query_values)
        return RawJsonInDB(**raw_json)

    async def get_raw_json_by_id(self, *, id: int) -> RawJsonInDB:
        raw_json = await self.db.fetch_one(query=GET_RAW_JSON_BY_ID_QUERY, values={"id": id})
        if not raw_json:
            return None
            
        return RawJsonInDB(**raw_json)
        
    async def get_all_raw_json(self) -> List[RawJsonInDB]:
        raw_json_records = await self.db.fetch_all(
            query=GET_ALL_RAW_JSON_QUERY,
        )
        return [RawJsonInDB(**l) for l in raw_json_records]

    async def update_raw_json(
        self, *, id: int, raw_json_update: RawJsonUpdate,
    ) -> RawJsonInDB:
        raw_json = await self.get_raw_json_by_id(id=id)
        if not raw_json:
            return None
        raw_json_update_params = raw_json.copy(
            update=raw_json_update.dict(exclude_unset=True),
        )
        try:
            updated_raw_json = await self.db.fetch_one(
                query=UPDATE_RAW_JSON_BY_ID_QUERY, 
                values=raw_json_update_params.dict(),
            )
            return RawJsonInDB(**updated_raw_json)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, 
                detail="Invalid update params.",
            )

    async def delete_raw_json_by_id(self, *, id: int) -> int:
        raw_json = await self.get_raw_json_by_id(id=id)
        if not raw_json:
            return None
        deleted_id = await self.db.execute(
            query=DELETE_RAW_JSON_BY_ID_QUERY, 
            values={"id": id},
        )
        return deleted_id