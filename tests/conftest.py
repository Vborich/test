import pytest
from httpx import AsyncClient
from tortoise import Tortoise

import src.settings as settings
from src.main import app


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
async def initialize_tests(request):
    await Tortoise.init(config=settings.DATABASE_TEST_CONFIG, _create_db=True)
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()
