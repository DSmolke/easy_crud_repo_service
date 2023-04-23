import os

from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool


def get_connection_pool(env_path: str) -> MySQLConnectionPool:
    """ Function creates and returns connection pool for MySQLDatabase using variables stored in .env file"""
    if load_dotenv(env_path, verbose=True):

        return MySQLConnectionPool(
            pool_name=os.getenv('POOL_NAME'),
            pool_size=int(os.getenv('POOL_SIZE')),
            pool_reset_session=bool(os.getenv('POOL_RESET_SESSION')),
            host=os.getenv('HOST'),
            database=os.getenv('DATABASE'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            port=int(os.getenv('PORT'))
        )
    raise ValueError("Env file does not exist")

