from typing import List
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.repositories.base import BaseRepository
from app.models.dispensaries import DispensaryCreate, DispensaryUpdate, DispensaryInDB


CREATE_DISPENSARY_FOR_COMPANY_QUERY = """
    INSERT INTO dispensaries (company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, cbd_url, address) 
    VALUES (:company_id, :flower_url, :pre_rolls_url, :vaporizers_url, :concentrates_url, :edibles_url, :tinctures_url, :cbd_url, :address)
    RETURNING id, company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, cbd_url, created_at, updated_at;
"""
GET_DISPENSARY_BY_COMPANY_ID_QUERY = """
    SELECT id, company_id, flower_url, pre_rolls_url, vaporizers_url, concentrates_url, edibles_url, tinctures_url, cbd_url, address, created_at, updated_at
    FROM dispensaries
    WHERE user_id = :user_id;
"""
class DispensariesRepository(BaseRepository):

    async def create_dispensary(self, *, new_dispensary: DispensaryCreate) -> DispensaryInDB:
        query_values = new_dispensary.dict()
        dispensary = await self.db.fetch_one(query=CREATE_DISPENSARY_FOR_COMPANY_QUERY, values=query_values)

        return DispensaryInDB(**dispensary)

    async def get_dispensary_by_id(self, *, id: int) -> DispensaryInDB:
        dispensary = await self.db.fetch_one(query=GET_DISPENSARY_BY_COMPANY_ID_QUERY, values={"id": id})
        if not dispensary:
            return None