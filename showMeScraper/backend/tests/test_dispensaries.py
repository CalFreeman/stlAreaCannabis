import pytest
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient
from app.models.dispensaries import DispensaryInDB


pytestmark = pytest.mark.asyncio

# class TestDispensaryRoutes:
#     @pytest.mark.asyncio
#     async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
#         res = await client.post(app.url_path_for("dispensary:create-dispensary"), json={"new_dispensary": new_dispensary})
#         assert res.status_code != HTTP_404_NOT_FOUND

