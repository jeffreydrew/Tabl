import os
import pytest
from .context import update_records
from update_records import *


# def test_create_empty_table():

#     # create empty table
#     create_empty_table()
#     # assert that table has been created
#     assert os.path.exists("databases/team_records.db")
#     # assert that there are 5 rows in the table
#     assert len(get_records()) == 6
#     # assert that the values in the table are correct


def test_create_teams_table():
    #set test database path
    test_path = 'tests/test_databases/team_records.db'
    # create teams table
    create_teams_table()
    # assert that table has been created
    assert os.path.exists('databases/team_records.db')
    # assert that there are 8 rows in the table
    assert len(get_records()) == 8
    # assert that the values in the table are correct
    assert get_records() == [
        ("1100", 0, 0),
        ("1200", 0, 0),
        ("1300", 0, 0),
        ("1301", 0, 0),
        ("1400", 0, 0),
        ("1401", 0, 0),
        ("1500", 0, 0),
        ("1600", 0, 0),
    ]


# def test_update_records():
#     # update records with team 1 win, team 2 loss, team 3 win, team 4 loss, team 5 win, team 6 loss
#     update_records("1", "win")
#     update_records("2", "loss")
#     update_records("3", "win")
#     update_records("4", "loss")
#     update_records("5", "win")
#     update_records("6", "loss")
#     # assert that the values in the table are correct
#     assert get_records() == [
#         ("1", 1, 0),
#         ("2", 0, 1),
#         ("3", 1, 0),
#         ("4", 0, 1),
#         ("5", 1, 0),
#         ("6", 0, 1),
#     ]


def test_clear_table():
    # clear table
    clear_table()
    # assert that there are 0 rows in the table
    assert len(get_records()) == 0
    # assert that the values in the table are correct
    assert get_records() == []
