import pytest
from pathlib import Path

from dbm_database_service.managers import MySQLDatabaseManager
from dbm_database_service.models.column import Column
from dbm_database_service.models.datatype import DataType
from dbm_database_service.models.table import Table

from easy_crud_repo_service.model.team import Team
from easy_crud_repo_service.repo.connections.builders import MySQLConnectionPoolBuilder
from easy_crud_repo_service.repo.crud_repo import CrudRepo




@pytest.fixture
def connection_tests() -> None:
    pool = MySQLConnectionPoolBuilder(f"{Path.cwd()}\\.env").set_new_port(3306).build()
    return pool

@pytest.fixture(autouse=True)
def create_teams_table(connection_tests):
    """ Creates teams table if not exists for further tests"""
    dbm = MySQLDatabaseManager(connection_tests)
    columns = [
        Column('id', DataType('int'), primary_key=True, auto_increment=True),
        Column('name', DataType('varchar', 255)),
        Column('points', DataType('int'))
    ]
    table = Table('teams', columns=columns, if_not_exist=True)
    dbm.create_table(table)

@pytest.fixture
def repo_tests(connection_tests):
    """ CrudRepo based on Team class """
    return CrudRepo(connection_tests, Team)
