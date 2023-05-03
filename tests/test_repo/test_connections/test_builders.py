import os
from pathlib import Path

import pytest

from easyvalid_data_validator.customexceptions.common import ValidationError
from mysql.connector.pooling import MySQLConnectionPool

from easy_crud_repo_service.repo.connections.builders import MySQLConnectionPoolBuilder


class TestWithValidCases:
    """ Valid cases for MySQLConnectionPoolBuilder """
    env_path = f"{Path.cwd()}//.env"

    def test_connection_with_absolute_path_provided(self) -> None:
        connection_pool = MySQLConnectionPoolBuilder(self.env_path).build()
        assert connection_pool.pool_name == "MYSQL_POOL"
        assert type(connection_pool) == MySQLConnectionPool

    def test_connection_with_invalid_path(self) -> None:
        with pytest.raises(ConnectionError) as e:
            MySQLConnectionPoolBuilder(fr"{os.getcwd()}\\fake.env")
        assert e.type == ConnectionError
        assert e.value.args[0] == "File is invalid or doesn't exist"

    def test_set_pool_name(self, basic_builder) -> None:
        basic_builder.set_pool_name('NEW_POOL')
        assert basic_builder._pool_config_["pool_name"] == "NEW_POOL"

    def test_set_pool_size(self, basic_builder) -> None:
        basic_builder.set_pool_size(1)
        assert basic_builder._pool_config_["pool_size"] == 1

    def test_set_pool_reset_session(self, basic_builder) -> None:
        basic_builder.set_pool_reset_session(False)
        assert basic_builder._pool_config_["pool_reset_session"] is False

    def test_set_new_host(self, basic_builder) -> None:
        basic_builder.set_new_host('127.0.0.2')
        assert basic_builder._pool_config_["host"] == '127.0.0.2'

    def test_set_new_database(self, basic_builder) -> None:
        basic_builder.set_new_database('db')
        assert basic_builder._pool_config_["database"] == 'db'

    def test_set_new_username(self, basic_builder) -> None:
        basic_builder.set_username('user1')
        assert basic_builder._pool_config_["user"] == 'user1'

    def test_set_new_password(self, basic_builder) -> None:
        basic_builder.set_password('pass')
        assert basic_builder._pool_config_["password"] == 'pass'

    def test_set_new_port(self, basic_builder) -> None:
        basic_builder.set_new_port(3309)
        assert basic_builder._pool_config_["port"] == 3309


class TestWithInvalidCases:
    """ Invalid cases for MySQLConnectionPoolBuilder """
    env_path = f"{Path.cwd()}//.env"

    def test_set_pool_name_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(absolute_dotenv_path=self.env_path).set_pool_name(1).build()
        assert e.value.args[0] == {'pool_name': ["Invalid type - isn't same type like compare type"]}

    def test_set_pool_size_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(self.env_path).set_pool_size('1').build()
        assert e.value.args[0] == {'pool_size': ["Invalid type - isn't same type like compare type"]}

    def test_set_pool_reset_session_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(self.env_path).set_pool_reset_session('False').build()
        assert e.value.args[0] == {'pool_reset_session': ["Invalid type - isn't same type like compare type"]}

    def test_set_new_host_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(self.env_path).set_new_host(127.1).build()
        assert e.value.args[0] == {'host': ["Invalid type - isn't same type like compare type"]}

    def test_set_new_database_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(self.env_path).set_new_database(1).build()
        assert e.value.args[0] == {'database': ["Invalid type - isn't same type like compare type"]}

    def test_set_new_username_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(self.env_path).set_username(1).build()
        assert e.value.args[0] == {'user': ["Invalid type - isn't same type like compare type"]}

    def test_set_new_password_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(self.env_path).set_password(1).build()
        assert e.value.args[0] == {'password': ["Invalid type - isn't same type like compare type"]}

    def test_set_new_port_with_invalid_arg(self) -> None:
        with pytest.raises(ValidationError) as e:
            MySQLConnectionPoolBuilder(self.env_path).set_new_port(3309.9).build()
        assert e.value.args[0] == {'port': ["Invalid type - isn't same type like compare type"]}
