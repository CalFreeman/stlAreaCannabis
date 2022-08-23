import pytest
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient
from app.models.dispensaries import DispensaryInDB


pytestmark = pytest.mark.asyncio

class TestDispensaryRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        new_dispensary = {"company_id": "test@email.io", "username": "test_username"}
        res = await client.post(app.url_path_for("dispensary:register-new-dispensary"), json={"new_dispensary": new_dispensary})
        assert res.status_code != HTTP_404_NOT_FOUND

