from typing import List
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.dispensaries import DispensaryCreate, DispensaryUpdate, DispensaryInDB


CREATE_DISPENSARY_FOR_COMPANY_QUERY = """
    INSERT INTO dispensaries (company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, topicals_url, cbd_url, address) 
    VALUES (:company_id, :flower_url, :pre_rolls_url, :vaporizers_url, :concentrates_url, :edibles_url, :tinctures_url, :cbd_url, :topicals_url, :address)
    RETURNING id, company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, topicals_url, cbd_url, created_at, updated_at;
"""

GET_DISPENSARY_BY_ID_QUERY = """
    SELECT id, company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, topicals_url, cbd_url, address, created_at, updated_at
    FROM dispensaries
    WHERE id = :id;
"""

GET_ALL_DISPENSARY_QUERY = """
    SELECT id, company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, topicals_url, cbd_url, address, created_at, updated_at
    FROM dispensaries
"""

UPDATE_DISPENSARY_BY_ID_QUERY = """
    UPDATE dispensaries
    SET flower_url          = :flower_url,
        pre_rolls_url       = :pre_rolls_url,
        vaporizers_url      = :vaporizers_url,
        concentrates_url    = :concentrates_url,
        edibles_url         = :edibles_url,
        tinctures_url       = :tinctures_url,
        cbd_url             = :cbd_url,
        topicals_url        = :topicals_url,
        address             = :address
    WHERE id = :id  
    RETURNING id, company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, topicals_url, cbd_url, address, created_at, updated_at;
"""

DELETE_DISPENSARY_BY_ID_QUERY = """
    DELETE FROM dispensaries  
    WHERE id = :id  
    RETURNING id;  
""" 
class DispensariesRepository(BaseRepository):

    async def create_dispensary(self, *, new_dispensary: DispensaryCreate) -> DispensaryInDB:
        query_values = new_dispensary.dict()
        dispensary = await self.db.fetch_one(query=CREATE_DISPENSARY_FOR_COMPANY_QUERY, values=query_values)

        return DispensaryInDB(**dispensary)

    async def get_dispensary_by_id(self, *, id: int) -> DispensaryInDB:
        dispensary = await self.db.fetch_one(query=GET_DISPENSARY_BY_ID_QUERY, values={"id": id})
        if not dispensary:
            return None
        return DispensaryInDB(**dispensary)

    async def get_all_dispensaries(self) -> List[DispensaryInDB]:
        dispensary_records = await self.db.fetch_all(
            query=GET_ALL_DISPENSARY_QUERY,
        )
        return [DispensaryInDB(**l) for l in dispensary_records]

    async def update_dispensary(self, *, id: int, dispensary_update: DispensaryUpdate) -> DispensaryInDB:
        dispensary = await self.get_dispensary_by_id(id=id)
        update_params = dispensary.copy(update=dispensary_update.dict(exclude_unset=True))

        updated_dispensary = await self.db.fetch_one(
            query=UPDATE_DISPENSARY_BY_ID_QUERY,
            values=update_params.dict(exclude={"company_id", "created_at", "updated_at"}),
        )
        print(updated_dispensary)
        return DispensaryInDB(**updated_dispensary)
        #return [DispensaryInDB(**updated_dispensary) for update_dispensary in updated_dispensary]

    async def delete_dispensary_by_id(self, *, id: int) -> int:
        dispensary = await self.get_dispensary_by_id(id=id)
        if not dispensary:
            return None
        deleted_id = await self.db.execute(
            query=DELETE_DISPENSARY_BY_ID_QUERY, 
            values={"id": id},
        )
        return deleted_id