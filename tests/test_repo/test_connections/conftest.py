from pathlib import Path

import pytest

from easy_crud_repo_service.repo.connections.builders import MySQLConnectionPoolBuilder


@pytest.fixture(scope='session')
def basic_builder():
    return MySQLConnectionPoolBuilder(f"{Path.cwd()}//.env")