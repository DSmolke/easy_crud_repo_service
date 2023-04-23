import os
from typing import Self

from dotenv import load_dotenv
from easyvalid_data_validator.constraints import Constraint
from easyvalid_data_validator.validator import validate_json_data
from mysql.connector.pooling import MySQLConnectionPool


class MySQLConnectionPoolBuilder:
    def __init__(self, env_path: str):
        if load_dotenv(env_path, verbose=True):
            self._pool_config_ = {
                'pool_name': os.getenv('POOL_NAME'),
                'pool_size': int(os.getenv('POOL_SIZE')),
                'pool_reset_session': bool(os.getenv('POOL_RESET_SESSION')),
                'host': os.getenv('HOST'),
                'database': os.getenv('DATABASE'),
                'user': os.getenv('USER'),
                'password': os.getenv('PASSWORD'),
                'port': int(os.getenv('PORT'))
            }
            validate_json_data(self._pool_config_, constraints={
                'pool_name': {Constraint.IS_TYPE: str},
                'pool_size': {Constraint.IS_TYPE: int},
                'pool_reset_session': {Constraint.IS_TYPE: bool},
                'host': {Constraint.IS_TYPE: str},
                'database': {Constraint.IS_TYPE: str},
                'user': {Constraint.IS_TYPE: str},
                'password': {Constraint.IS_TYPE: str},
                'port': {Constraint.IS_TYPE: int},
            })
        else:
            raise ValueError("Env file does not exist")

    def set_pool_name(self, new_pool_name: str) -> Self:
        self._pool_config_['pool_name'] = new_pool_name
        return self

    def set_pool_size(self, new_size: int) -> Self:
        self._pool_config_['pool_size'] = new_size
        return self

    def set_pool_reset_session(self, new_pool_reset_session: bool) -> Self:
        self._pool_config_['pool_reset_session'] = new_pool_reset_session
        return self

    def set_new_host(self, new_host: str) -> Self:
        self._pool_config_['host'] = new_host
        return self

    def set_new_database(self, new_database: str) -> Self:
        self._pool_config_['database'] = new_database
        return self

    def set_username(self, new_username: str) -> Self:
        self._pool_config_['user'] = new_username
        return self

    def set_password(self, new_password: str) -> Self:
        self._pool_config_['password'] = new_password
        return self

    def set_new_port(self, new_port: int) -> Self:
        self._pool_config_['port'] = new_port
        return self

    def build(self) -> MySQLConnectionPool:
        validate_json_data(self._pool_config_, constraints={
            'pool_name': {Constraint.IS_TYPE: str},
            'pool_size': {Constraint.IS_TYPE: int},
            'pool_reset_session': {Constraint.IS_TYPE: bool},
            'host': {Constraint.IS_TYPE: str},
            'database': {Constraint.IS_TYPE: str},
            'user': {Constraint.IS_TYPE: str},
            'password': {Constraint.IS_TYPE: str},
            'port': {Constraint.IS_TYPE: int},
        })
        return MySQLConnectionPool(**self._pool_config_)
