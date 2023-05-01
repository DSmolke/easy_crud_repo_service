import inflection
import logging

from datetime import datetime, date
from dotenv import load_dotenv
from mysql.connector import pooling, Error
from typing import Any
from contextlib import contextmanager

logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

load_dotenv()


class CrudRepo:

    def __init__(self, connection_pool: pooling.MySQLConnectionPool,  entity: type) -> None:
        self._connection_pool = connection_pool
        self._entity = entity
        self._entity_type = type(entity())

    @contextmanager
    def _get_cursor_object(self):
        connection_object = self._connection_pool.get_connection()

        try:
            if connection_object.is_connected():
                cursor_object = connection_object.cursor()
                logging.debug(cursor_object)
                yield cursor_object
                logging.debug(cursor_object)
                connection_object.commit()
        except Error as e:
            connection_object.rollback()
        finally:
            if connection_object.is_connected():
                cursor_object.close()
                connection_object.close()

    def _table_name(self) -> str:
        # ta biblioteka pomaga w pracy na stringach, .tableize(), jeśli dostanie Car to zwróci cars
        return inflection.tableize(self._entity_type.__name__)

    def _fields_names(self) -> list[str]:
        # dict zwraca namespaces, keys() wyciąga tylko nazwy
        return list(self._entity().__dict__.keys())

    def _column_names_for_insert(self) -> str:
        # zwraca wszystkie nazwy poza id
        return ', '.join([field for field in self._fields_names() if field.lower() != 'id'])

    def insert(self, item: Any) -> int:
        with self._get_cursor_object() as cur:
            sql = f'insert into {self._table_name()} ' \
                  f'({self._column_names_for_insert()}) ' \
                  f'values ({self._column_values_for_insert(item)});'
            cur.execute(sql)
            return cur.lastrowid

    def insert_many(self, items: list[Any]) -> list[int]:
        with self._get_cursor_object() as cur:
            values = ", ".join([f"({CrudRepo._column_values_for_insert(item)})" for item in items])
            sql = f"insert into {self._table_name()} ({self._column_names_for_insert()}) values {values}"
            cur.execute(sql)
            return [item.id for item in self.find_n_last(len(items))]

    def update(self, item_id: int, item: Any) -> Any:
        with self._get_cursor_object() as cur:
            sql = f"update {self._table_name()} set {CrudRepo._column_names_and_values_for_update(item)} where id = {item_id}"
            logging.debug(sql)
            cur.execute(sql)
            return self.find_one(item_id)

    def find_n_last(self, n) -> list[Any]:
        with self._get_cursor_object() as cur:
            sql = f'select * from {self._table_name()} order by id desc limit {n}'
            cur.execute(sql)
            return [self._entity(*row) for row in cur.fetchall()]

    def find_one(self, item_id: int) -> Any:
        with self._get_cursor_object() as cur:
            sql = f"select * from {self._table_name()} where id = {item_id}"
            cur.execute(sql)
            result = cur.fetchone()
            if not result:
                raise RuntimeError(f"Item with id {item_id} wasn't found")
            return self._entity(*result)

    def find_all(self) -> list[Any]:
        with self._get_cursor_object() as cur:
            sql = f"select * from {self._table_name()}"
            cur.execute(sql)
            return [self._entity(*row) for row in cur.fetchall()]

    def delete_one(self, item_id) -> int:
        with self._get_cursor_object() as cur:
            sql = f"delete from {self._table_name()} where id = {item_id}"
            self.find_one(item_id)
            cur.execute(sql)
            return item_id

    def delete_all(self) -> list[int]:
        with self._get_cursor_object() as cur:
            all_deleted_items = [item.id for item in self.find_all()]
            sql = f'delete from {self._table_name()} where id >= 1'
            cur.execute(sql)
            return all_deleted_items

    @classmethod
    def _column_values_for_insert(cls, item: Any) -> str:

        def to_str(entry: Any) -> str:
            # funkcja pomocnicza, która zwraca f-string z wartością jeżeli jest ona napisem albo datą
            return f"'{entry[1]}'" if isinstance(entry[1], (str, datetime, date)) else str(entry[1])

        return ", ".join([to_str(entry) for entry in item.__dict__.items() if entry[0].lower() != 'id'])

    @classmethod
    def _column_names_and_values_for_update(cls, entity) -> str:
        def to_str(entry: Any) -> str:
            return entry[0] + '=' + (f"'{entry[1]}'" if isinstance(entry[1], (str, datetime, date)) else str(entry[1]))

        return ', '.join([to_str(item) for item in entity.__dict__.items() if item[0].lower() != 'id'])


def main() -> None:
    pass


if __name__ == "__main__":
    main()
