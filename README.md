# easy-crud-repo-service
Package that allows user to use any object as entity and process basic CRUD operations on database.

## Installation
[PyPI](https://pypi.org/project/easy-crud-repo-service/)

Using pip:
```bash
  pip install easy-crud-repo-service
```
Using poetry:
```bash
  poetry add easy-crud-repo-service
```
Using pipenv:
```bash
  pipenv install easy-crud-repo-service
```

## TESTS

### 1. Clone repository and enter main directory:
```angular2html
    git clone https://github.com/DSmolke/easy_crud_repo_service
    cd easy_crud_repo_service
```

### 1. Make sure your docker is running and port 3306 is empty, and run docker-compose command
```angular2html
    docker-compose up -d
    cd tests
```
### 3. Run tests using:
####Poetry:
```angular2html
    poetry install
    poetry shell    
    cd tests
    poetry run pytest -vv
```
* update protects from decoding errors
* tests take around 15s because of database and .env files

####Pipenv:
```angular2html
    pipenv shell 
    cd tests
    pipenv run pytest -vv
```

####Pip:
```angular2html
    pip install mysql-connector-python
    pip install python-dotenv
    pip install easyvalid-data-validator
    pip install gdown
    pip install pytest
    cd tests
    pytest -vv
```

## Basic usage
Having existing database server, or mysql container, we want to create new table, add columns to existing table or
do any operation on database.

###1. Step - prepare .env file
Please download .env file template - > [link](https://drive.google.com/drive/folders/1Ed1gQlnVKnk7hLUMWTGJ0W4l5b-yZPjs?usp=sharing)

Edit file according to your needs.
```angular2html
POOL_NAME=TEST
POOL_SIZE=5
POOL_RESET_SESSION=True
HOST=localhost
DATABASE=test_db
USER=user
PASSWORD=user
PORT=3306
```

Copy its absolute path and keep it for later use.

###2. Step - Import all necessary objects
```angular2html
from dbm_database_service.models.column import Column
from dbm_database_service.models.table import Table
from dbm_database_service.models.datatype import DataType
from dbm_database_service.connectors import MySQLConnectionPoolBuilder
from dbm_database_service.managers import MySQLDatabaseManager
```

###3. Step - Create new MySQLConnectionPoolBuilder with prepared .env path
```angular2html
dbm1 = MySQLConnectionPoolBuilder(r'C:\Users\Omen i5\Desktop\PROJEKTY\dbm_database_service\tests\.env')
```

###4. Step - Create new MySQLDatabaseManager using object prepared in previous step
```angular2html
database_manager = MySQLDatabaseManager(dbm1.build())
```

###5. Step - Add new table into database:
```angular2html
database_manager.create_table(
    Table('jeans', [
        Column('id', datatype=DataType('int')),
        Column('brand', datatype=DataType('varchar', 255))
    ]))
```

###6. Step - Check your database, new table should be waiting for you!

## Objects

### Datatype
Contains valid MySQL datatype name with or without corresponding value

#### Variations examples:
```angular2html
int -> DataType('int')
varchar(255) -> DataType('varchar', 255)
decimal(5, 2) -> DataType('decimal', (5, 2))
```

Full code:
```angular2html
@dataclass
class DataType:
    """ Objects stores information that creates string representation of valid MySQL datatype"""
    name: str
    corresponding_value: tuple | int = None

    def __post_init__(self) -> None:
        """ Checks if name is valid for MySQL syntax and if corresponding value is valid to coexist with name """
        if self.name.upper() not in Settings.valid_mysql_datatypes:
            raise ValueError('Invalid datatype name')
        if self.corresponding_value is not None and self.name.upper() not in Settings.mysql_datatypes_with_corresponding_value:
            raise ValueError("Provided datatype shouldn't have corresponding value")

    def __str__(self) -> str:
        """ Will be parsed in other objects. Outcome is valid sql string describing datatype"""
        single_value = isinstance(self.corresponding_value, int)

        corresponding_value_str = "" if self.corresponding_value is None else \
            f"({self.corresponding_value if single_value else ', '.join([str(v) for v in self.corresponding_value])})"
        return f"{self.name}{corresponding_value_str}"

```

### Column
Contain informations about MySQL column
#### Example:
```angular2html
Column('id', datatype=DataType('int'))
```
Full list of arguments:
```angular2html
    name: str
    datatype: DataType
    primary_key: bool = False
    autoincrement: bool = False
    unique: bool = False
    default: Any = None
    not_null: bool = False
```

Full code:
```angular2html
@dataclass
class Column:
    """ Needs minimum of name and datatype to parse and can be extended by primary key, autoincrement, unique, default, not_null"""
    name: str
    datatype: DataType
    primary_key: bool = False
    autoincrement: bool = False
    unique: bool = False
    default: Any = None
    not_null: bool = False

    def __post_init__(self) -> None:
        """ Validates if provided arguments are valid """
        namespaces = self.__dict__
        constraints = {
            "name": {Constraint.STRING_REGEX: r'^[a-zA-Z_][a-zA-Z0-9_]{1,64}$'},
            "primary_key": {Constraint.IS_TYPE: bool},
            "autoincrement": {Constraint.IS_TYPE: bool},
            "unique": {Constraint.IS_TYPE: bool},
            "not_null": {Constraint.IS_TYPE: bool}
        }
        validate_json_data(namespaces, constraints)

    def __str__(self):
        """ Will be parsed in other objects. Outcome is valid sql string describing column """
        return f"{self.name} {self.datatype}" \
               f"{' primary key' if self.primary_key else ''}" \
               f"{' autoincrement' if self.autoincrement else ''}" \
               f"{' unique' if self.unique else ''}" \
               f"{' not null' if self.not_null else ''}" \
               f"{f' default {self.default}' if self.default else ''}"
```

### Table
Contains information of Table that we are willing to create

#### Example:
```angular2html
Table('cats', columns=[
    Column('id', datatype=DataType('int')),
    Column('name', datatype=DataType('varchar', 255))
])
```
Full list of arguments:
```angular2html
    name: str
    columns: list[Column]
    if_not_exist: bool = False
    temporary: bool = False
```
Full code:
```angular2html
@dataclass
class Table:
    name: str
    columns: list[Column]
    if_not_exist: bool = False
    temporary: bool = False

    def __str__(self) -> str:
        """ Will be parsed in other objects. Outcome is valid SQL Create Table expression """
        return f"create{' temporary' if self.temporary else ''} table" \
               f"{' if not exists' if self.if_not_exist else ''}" \
               f" {self.name}(" \
               f"{', '.join([str(c) for c in self.columns])});" \


    def drop_statement(self) -> str:
        """ Auxiliary method, that returns expression of sql drop table if exist with name stored in instance """
        return f"drop table if exists {self.name}"

    def alter_statement(self) -> str:
        """ Auxiliary method, that returns expression of sql alter table with name stored in instance """
        return f"alter table {self.name}"

```

## Connectors
There are two types of connectors available. get_connection_pool and MySQLConnectionPoolBuilder.
They differ in philosophy, but work on the same principle. To load environmental variables needed for db connection
and return connection pool.

### get_connection_pool
#### Example:
```angular2html
    get_connection_pool() -> function will look for .env file in same location
    # or
    get_connection_pool(<ABSOLUTE-PATH>) -> full path of .env file can be provided
```

### MySQLConnectionPoolBuilder
#### Example:
```angular2html
    # The principle for .env path is same
    builder = MySQLConnectionPoolBuilder() -> function will look for .env file in same location
    
    # you can modify credentials during program flow
    builder.set_new_port(3307).add_new_password('password')

    # when you are ready, you can build connection pool
    database_manager = builder.build()
```

## MySQLDatabaseManager

It works on connection pool and allows user to create, modify, drop tables as well as 
execute custom sql for development use

### Methods:

#### _get_cursor_object:

Example:
```angular2html
     with self._get_cursor_object() as cur:
            cur.execute(str(sql))
            return cur.fetchall()
```
Context manager that allows us to work on 'with' statement to avoid problems when errors occur
during operations on cursor

Full code:
```angular2html
        def _get_cursor_object(self):
        """ Custom context manager for db cursor. Uses object's connection pool to establish connection and later on cursor """
        connection_object = self._connection_pool.get_connection()
        try:
            if connection_object.is_connected():
                cursor_object = connection_object.cursor()
                yield cursor_object
                connection_object.commit()
        except Error as e:
            connection_object.rollback()
        finally:
            if connection_object.is_connected():
                cursor_object.close()
                connection_object.close()
```

#### create_table:

Example:
```angular2html
    database_manager.create_table(
    Table('jeans', [
        Column('id', datatype=DataType('int')),
        Column('brand', datatype=DataType('varchar', 255))
    ]))
```
Creates new table using Table instance.

Full code:
```angular2html
    def create_table(self, table: Table) -> None:
        """
        Creates table in database using Table instance as a provider of specification of the table
        :param table: Table instance
        :return: None
        """
        if not isinstance(table, Table):
            raise ValueError(f'Provided argument has to be Table object')
        with self._get_cursor_object() as cur:
            cur.execute(str(table))
```

#### drop_table_if_exists:

Example:
```angular2html
    database_manager.drop_table_if_exists('jeans')
    # or
    database_manager.drop_table_if_exists(
        Table('jeans', [
        Column('id', datatype=DataType('int')),
        Column('brand', datatype=DataType('varchar', 255))
    ]))
```
User can use Table object or table name to delete it from database

Full code:
```angular2html
def drop_table_if_exists(self, table: str | Table) -> None:
    """
    Drops a table if any exists in database. Does not cause error as long as connection is valid
    :param table: table name or Table instance
    :return: None
    """
    with self._get_cursor_object() as cur:
        if type(table) == str:
            cur.execute(f"drop table if exists {table}")
        elif isinstance(table, Table):
            cur.execute(table.drop_statement())
        else:
            raise ValueError(f'Provided argument has to be Table object')
```

#### add_columns:

Example:
```angular2html
    database_manager.drop_table_if_exists('jeans')
    # or
    database_manager.add_columns([
        Column('model', datatype=DataType('varchar', 255)),
        Column('price'', datatype=DataType('decimal', (5,2)))
    ])
```
User can use Column objects to add new columns into existing table 

Full code:
```angular2html
def add_columns(self, table: str | Table, columns: list[Column]) -> None:
    """
    Ads columns into existing table. Can work on one or more Columns
    :param table: table name or Table instance
    :param columns: list of Column instances
    :return: None
    """
    if not all([True if isinstance(c, Column) else False for c in columns]):
        raise ValueError("Some values in 'columns' argument are not Column instances")
    add_statement = ", ".join([f"add column {str(c)}" for c in columns])
    with self._get_cursor_object() as cur:
        if type(table) == str:
            cur.execute(f"alter {table} {add_statement}")
        elif isinstance(table, Table):
            cur.execute(f"{table.alter_statement()} {add_statement}")
        else:
            raise ValueError(f'Provided argument has to be Table object')
```

#### dev_console:

Example:
```angular2html
    database_manager.dev_console('use test_tb;')
```
Method allows us to use custom sql statements.

Full code:
```angular2html
    def dev_console(self, sql: str) -> None:
        """ Utility made for custom development using sql syntax"""
        with self._get_cursor_object() as cur:
            cur.execute(str(sql))
            return cur.fetchall()
```
