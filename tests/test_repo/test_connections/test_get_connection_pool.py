import pytest
from pathlib import Path

from mysql.connector.pooling import MySQLConnectionPool

from easy_crud_repo_service.repo.connections.get_connection_pool import get_connection_pool


class TestGetConnectionPool:
    env_path = f"{Path.cwd()}//.env"

    def test_connection_with_absolute_path_provided(self) -> None:
        connection_pool = get_connection_pool(env_path=self.env_path)
        assert connection_pool.pool_name == "MYSQL_POOL"
        assert type(connection_pool) == MySQLConnectionPool

    def test_connection_with_invalid_path(self) -> None:
        with pytest.raises(ValueError) as e:
            get_connection_pool(f"{Path.cwd()}\\fake.env")
        assert e.type == ValueError
        assert e.value.args[0] == "Env file does not exist"
