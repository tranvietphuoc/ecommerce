from ecommerce import create_app
from ecommerce.config import TestingConfig
import pytest
import os


@pytest.fixture
def client():
    app = create_app(config_class=TestingConfig)

    with app.test_client() as client:
        yield client

    os.close(TestingConfig.db_fd)
    os.unlink(TestingConfig.db_path)


def test_empty_db(client):
    """start with a blank database"""

    rv = client.get("/")
    assert b'No entries here so far' in rv.data
