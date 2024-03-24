import os

import pytest
from starlette.testclient import TestClient

from app.main import create_application
from app.config import get_settings, Settings
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import initializer, finalizer
import asyncio

def get_settings_override():
    return Settings(testing=True, database_url=os.environ.get("DATABASE_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()  # new
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:  # updated

        # testing
        yield test_client

    # tear down



# Set up the event loop for the entire test suite

@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL_TEST"),
        modules={"models": ["app.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down