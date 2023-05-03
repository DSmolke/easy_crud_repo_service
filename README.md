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
    pip install inflection
    pip install pytest
    pip install dbm-database-service
    pip install coverage
    cd tests
    pytest -vv
```

## Basic usage
Having existing database server, or mysql container, we want to make some 

###1. Step - prepare .env file
Please download .env file template - > [link](https://drive.google.com/drive/folders/1Ed1gQlnVKnk7hLUMWTGJ0W4l5b-yZPjs?usp=sharing)

Edit file according to your needs and place it in same directory.
```angular2html
POOL_NAME=TEST
POOL_SIZE=5
POOL_RESET_SESSION=True
HOST=localhost
DATABASE=db_1
USER=root
PASSWORD=root
PORT=3306
```



###2. Step - Import all necessary objects
```angular2html
from pathlib import Path
from easy_crud_repo_service.repo.crud_repo import CrudRepo
from easy_crud_repo_service.repo.connections.builders import MySQLConnectionPoolBuilder
```

###3. Step - Create new MySQLConnectionPoolBuilder
```angular2html
dbm_builder = MySQLConnectionPoolBuilder(f"{Path.cwd()}\\.env")
```

###4. Step - Create new MySQLDatabaseManager using object prepared in previous step
```angular2html
dbm = dbm_builder.build()
```

###5. Create crud repo according to your needs
```angular2html
# Entity that you want to work on
@dataclass
class Team:
    id: int = 0
    name: str = ""
    points: int = 0

crud_repo = CrudRepo(dbm, Team)
```

###5. Make operations on database table
```angular2html
crud_repo.insert(Team(1, 'REAL MADRIT', 20))
print(crud_repo.find_all())
```

## Objects


## Connectors
There are two types of connectors available. get_connection_pool and MySQLConnectionPoolBuilder.
They differ in philosophy, but work on the same principle. To load environmental variables needed for db connection
and return connection pool.

### get_connection_pool
#### Example:
```angular2html
    get_connection_pool(<ABSOLUTE-PATH>) -> full path of .env file can be provided
```

### MySQLConnectionPoolBuilder
#### Example:
```angular2html
    # The principle for .env path is same
    builder = MySQLConnectionPoolBuilder(<ABSOLUTE-PATH>)
    
    # you can modify credentials during program flow
    builder.set_new_port(3307).add_new_password('password')

    # when you are ready, you can build connection pool
    database_manager = builder.build()
```

## CrudRepo

It takes class as an entity and uses its properties to prepare sql statements for communication with database

```angular2html
class CrudRepo:

    def __init__(self, connection_pool: pooling.MySQLConnectionPool,  entity: type) -> None:
        self._connection_pool = connection_pool
        self._entity = entity
        self._entity_type = type(entity())
```

### Methods:

#### _get_cursor_object:

Example:
```angular2html
    @contextmanager
    def _get_cursor_object(self):
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
Context manager that allows us to work on 'with' statement to avoid problems when errors occur
during operations on cursor

#### _table_name:

Example:
```angular2html
    def _table_name(self) -> str:
        return inflection.tableize(self._entity_type.__name__)
```
Creates valid MySQL table name by adding s at the end of the class name as well as lowering letters case
Team -> teams


#### _fields_names:

Example:
```angular2html
    def _fields_names(self) -> list[str]:
        return list(self._entity().__dict__.keys())
```
Method returns names of objects attributes as a list


#### _column_names_for_insert:

Example:
```angular2html
    def _column_names_for_insert(self) -> str:
        return ', '.join([field for field in self._fields_names() if field.lower() != 'id'])
```
Returns all names accept id


#### insert:

Example:
```angular2html
    def insert(self, item: Any) -> int:
        with self._get_cursor_object() as cur:
            sql = f'insert into {self._table_name()} ' \
                  f'({self._column_names_for_insert()}) ' \
                  f'values ({self._column_values_for_insert(item)});'
            cur.execute(sql)
            return cur.lastrowid
```
Method inserts object into table and return its id

#### insert_many:

Example:
```angular2html
   def insert_many(self, items: list[Any]) -> list[int]:
        with self._get_cursor_object() as cur:
            values = ", ".join([f"({CrudRepo._column_values_for_insert(item)})" for item in items])
            sql = f"insert into {self._table_name()} ({self._column_names_for_insert()}) values {values}"
            cur.execute(sql)
            return [item.id for item in self.find_n_last(len(items))]
```
Method inserts objects into table and return theirs ids

#### update:

Example:
```angular2html
   def update(self, item_id: int, item: Any) -> Any:
        with self._get_cursor_object() as cur:
            sql = f"update {self._table_name()} set {CrudRepo._column_names_and_values_for_update(item)} where id = {item_id}"
            cur.execute(sql)
            return self.find_one(item_id)

```
Method updates row that has specified id with provided object

#### find_n_last:

Example:
```angular2html
   def find_n_last(self, n) -> list[Any]:
        with self._get_cursor_object() as cur:
            sql = f'select * from {self._table_name()} order by id desc limit {n}'
            cur.execute(sql)
            return [self._entity(*row) for row in cur.fetchall()]

```
Method finds n last rows of table that we are working on

#### find_one:

Example:
```angular2html
   def find_one(self, item_id: int) -> Any:
        with self._get_cursor_object() as cur:
            sql = f"select * from {self._table_name()} where id = {item_id}"
            cur.execute(sql)
            result = cur.fetchone()
            if not result:
                raise RuntimeError(f"Item with id {item_id} wasn't found")
            return self._entity(*result)

```
Method finds row by id

#### find_all:

Example:
```angular2html
   def find_all(self) -> list[Any]:
        with self._get_cursor_object() as cur:
            sql = f"select * from {self._table_name()}"
            cur.execute(sql)
            return [self._entity(*row) for row in cur.fetchall()]

```
Method finds all rows in the table

#### delete_one:

Example:
```angular2html
   def delete_one(self, item_id) -> int:
        with self._get_cursor_object() as cur:
            sql = f"delete from {self._table_name()} where id = {item_id}"
            self.find_one(item_id)
            cur.execute(sql)
            return item_id

```
Method deletes one row using provided id

#### delete_all:

Example:
```angular2html
    def delete_all(self) -> list[int]:
        with self._get_cursor_object() as cur:
            all_deleted_items = [item.id for item in self.find_all()]
            sql = f'delete from {self._table_name()} where id >= 1'
            cur.execute(sql)
            return all_deleted_items

```
Method deletes all rows from table

#### _column_values_for_insert:

Example:
```angular2html
    @classmethod
    def _column_values_for_insert(cls, item: Any) -> str:

        def to_str(entry: Any) -> str:
            return f"'{entry[1]}'" if isinstance(entry[1], (str, datetime, date)) else str(entry[1])

        return ", ".join([to_str(entry) for entry in item.__dict__.items() if entry[0].lower() != 'id'])

```
Method creates expression with values that we want to put into sql. (All accept id)

#### _column_names_and_values_for_update:

Example:
```angular2html
    @classmethod
    def _column_names_and_values_for_update(cls, entity) -> str:
        def to_str(entry: Any) -> str:
            return entry[0] + '=' + (f"'{entry[1]}'" if isinstance(entry[1], (str, datetime, date)) else str(entry[1]))

        return ', '.join([to_str(item) for item in entity.__dict__.items() if item[0].lower() != 'id'])

```
Method creates expression that will be responsible for updating row values. (All accept id)
