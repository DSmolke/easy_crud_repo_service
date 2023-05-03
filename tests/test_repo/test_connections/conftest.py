from pathlib import Path

import pytest

from easy_crud_repo_service.repo.connections.builders import MySQLConnectionPoolBuilder


@pytest.fixture(scope='session')
def basic_builder():
    """ Builder created with .env file based in /tests directory"""
    return MySQLConnectionPoolBuilder(f"{Path.cwd()}//.env")