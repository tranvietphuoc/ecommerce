import os
import tempfile
from ecommerce import create_app
from ecommerce.config import TestingConfig
import pytest


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkdstemp()
    app = create_app(config_class=TestingConfig)
    app.config['DATABASE': db_path]

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)
