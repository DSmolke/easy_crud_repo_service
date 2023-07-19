import re
import logging
from datetime import date

from easy_crud_repo_service.model.car import Car
from easy_crud_repo_service.model.order import Order

logging.basicConfig(level=logging.INFO)
from easy_crud_repo_service.model.team import Team
from easy_crud_repo_service.repo.crud_repo import CrudRepo


class TestCrudRepo:
    def test_if_insert_works_good(self, repo_tests):
        team = Team(name='JOHN', points=10)
        res = repo_tests.insert(team)
        # If there is no error, insert works correctly
        assert res >= 1

    def test_table_name(self, repo_tests) -> None:
        table_name = repo_tests._table_name()
        assert table_name == 'teams'
        assert type(table_name) == str
        assert re.match(r'\D+s', table_name)

    def test_field_names(self, repo_tests) -> None:
        fields_names = repo_tests._fields_names()
        assert type(fields_names) == list
        assert all(True for name in fields_names if type(name) == str)
        assert len(fields_names) == 3
        assert all(True for name in fields_names if re.match(r'\D+', name))

    def test_column_names_for_insert(self, repo_tests) -> None:
        columns_for_insert = repo_tests._column_names_for_insert()
        assert type(columns_for_insert) == str
        assert 'id' not in columns_for_insert
        assert all([name in columns_for_insert for name in ['name', 'points']])

    def test_insert_with_valid_entity(self, repo_tests) -> None:
        team = Team(name='JOHN', points=10)
        res = repo_tests.insert(team)
        # If there is no error, insert works correctly
        assert res > 1

    def test_insert_many_with_valid_entities(self, repo_tests) -> None:
        teams = [Team(name='JOHN', points=10), Team(name='MADRIT', points=2)]
        res = repo_tests.insert_many(teams)
        assert all([True for n in res if n > 0])
        assert len(res) == 2

    def test_update_with_valid_entity(self, repo_tests) -> None:
        team_for_insert = Team('Malaga', 30)
        team_for_update = Team('Malaga', 20)
        team_id = repo_tests.insert(team_for_insert)
        obtained_team = repo_tests.update(team_id, team_for_update)
        assert obtained_team.id == team_id
        assert obtained_team.points == team_for_update.points and obtained_team.points != team_for_insert

    def test_valid_find_n_last(self, repo_tests) -> None:
        teams = repo_tests.find_n_last(2)
        assert len(teams) == 2
        assert all(True for team in teams if type(team) == Team)

    def test_valid_find_one(self, repo_tests) -> None:
        team_for_insert = Team('Malaga', 30)
        insert_res = repo_tests.insert(team_for_insert)
        found_team = repo_tests.find_one(insert_res)
        assert found_team.id == insert_res

    def test_valid_find_all(self, repo_tests) -> None:
        teams = repo_tests.find_all()
        assert len(teams) > 0
        assert all([True for team in teams if type(team) == Team])

    def test_valid_delete_one(self, repo_tests) -> None:
        team_for_insert = Team('Malaga', 30)
        insert_res = repo_tests.insert(team_for_insert)
        deleted__id = repo_tests.delete_one(insert_res)
        assert insert_res == deleted__id

    def test_valid_delete_many(self, repo_tests) -> None:
        teams_for_insert = [Team(None, 'A', 30), Team(None, 'B', 30), Team(None, 'C', 30)]
        insert_res = repo_tests.insert_many(teams_for_insert)
        teams_for_delete = [Team(insert_res[0], 'A', 30), Team(insert_res[1], 'B', 30), Team(insert_res[2], 'C', 30)]
        deleted_ids = repo_tests.delete_many(teams_for_delete)

        assert insert_res == deleted_ids

    def test_valid_delete_all(self, repo_tests) -> None:
        deleted_ids = repo_tests.delete_all()
        assert len(deleted_ids) > 0

    def test_valid_column_values_for_insert(self) -> None:
        columns_for_insert = CrudRepo._column_values_for_insert(Team(1, 'MALAGA', 10))
        assert type(columns_for_insert) == str
        assert 'id' not in columns_for_insert

    def test_valid_colum_names_and_values_for_update(self) -> None:
        column_names_and_values_for_update = CrudRepo._column_names_and_values_for_update(Team(1, 'MALAGA', 10))
        assert type(column_names_and_values_for_update) == str
        assert column_names_and_values_for_update == "name='MALAGA', points=10"

    def test_valid_colum_names_and_values_for_update_with_date_field(self) -> None:
        column_names_and_values_for_update = CrudRepo._column_names_and_values_for_update(Order(1, date(2022, 6, 12)))
        assert type(column_names_and_values_for_update) == str
        assert column_names_and_values_for_update == "order_date='2022-06-12'"

    def test_valid_colum_names_and_values_for_car_object(self) -> None:
        column_names_and_values_for_update = CrudRepo._column_names_and_values_for_update(Car(1, "WW12345", date(2012, 6, 22), 'xxxxxxxxxxxxxxxxx', 'BMW', 'M5'))
        logging.info(column_names_and_values_for_update)
        # assert type(column_names_and_values_for_update) == str
        # assert column_names_and_values_for_update == "order_date='2022-06-12'"
