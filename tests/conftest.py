import os

os.environ["ENV"] = "test"

import pytest
from fastapi.testclient import TestClient

from db.seed import seed
from main import app

@pytest.fixture(autouse=True)
def seed_test_db():
    database = os.getenv("PGDATABASE", "")
    assert database.endswith("_test"), f"Refusing to seed non-test database {database!r}"

    seed()

@pytest.fixture
def client():
    return TestClient(app)

