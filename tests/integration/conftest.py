from shutil import copy


import pytest
from app import TITANIC_DB, create_app


@pytest.fixture
def client(tmpdir):
    test_path = "/Users/amoshochman/PycharmProjects/titanic_flask_2/tests"

    copy("/Users/amoshochman/PycharmProjects/titanic_flask_2/titanic.db", test_path)#tmpdir.dirpath())

    temp_db_file = f"sqlite:///{test_path}/{TITANIC_DB}"

    app = create_app(temp_db_file)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
