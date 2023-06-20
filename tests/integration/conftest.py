from shutil import copy


import pytest
from app import create_app
from constants import PROJECT_ROOT, TITANIC_DB


@pytest.fixture
def client(tmpdir):
    copy(f"{PROJECT_ROOT}/{TITANIC_DB}", tmpdir.dirpath())
    temp_db_file = f"sqlite:///{tmpdir.dirpath()}/{TITANIC_DB}"
    app = create_app(temp_db_file)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
