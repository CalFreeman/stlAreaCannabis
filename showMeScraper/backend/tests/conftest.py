import warnings
import os

import pytest
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

from app.models.companies import CompanyCreate, CompanyInDB
from app.db.repositories.companies import CompaniesRepository

from app.models.dispensaries import DispensaryCreate, DispensaryInDB
from app.db.repositories.dispensaries import DispensariesRepository

import alembic
from alembic.config import Config


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application

    return  get_application()

# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db

@pytest.fixture
async def test_company(db: Database) -> CompanyInDB:
    company_repo = CompaniesRepository(db)
    new_company = CompanyCreate(
        name="fake company name"
    )
    return await company_repo.create_company(new_company=new_company)

@pytest.fixture
async def test_dispensary(db: Database) -> DispensaryInDB:
    new_dispensary = DispensaryCreate(company_id=1, flower_url="test")

    dispensaries_repo = DispensariesRepository(db)

    existing_dispensary = await dispensaries_repo.get_dispensary_by_id(company_id=new_dispensary.company_id)
    if existing_dispensary:
        return existing_dispensary

    return await dispensaries_repo.register_new_dispensary(new_dispensary=new_dispensary)

# Make requests in our tests
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client

