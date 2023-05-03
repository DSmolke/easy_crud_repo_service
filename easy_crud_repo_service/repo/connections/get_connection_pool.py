import os

from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool


def get_connection_pool(absolute_dotenv_path: str) -> MySQLConnectionPool:
    """ Function creates and returns connection pool for MySQLDatabase using variables stored in .env file"""
    for v in ['POOL_NAME', 'POOL_SIZE', 'POOL_RESET_SESSION', 'HOST', 'DATABASE', 'USER', 'PASSWORD', 'PORT']:
        if v in os.environ:
            del os.environ[v]
    # loading of .env file
    load_dotenv(absolute_dotenv_path, override=True)
    # attempt of creation a new connection pool
    try:
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
    except TypeError:
        raise ConnectionError("File is invalid or doesn't exist")

