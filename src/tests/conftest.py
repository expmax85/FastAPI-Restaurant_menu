import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from src.main import app


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_app():
    async with AsyncClient(app=app, base_url='http://test.io') as client:
        yield client
