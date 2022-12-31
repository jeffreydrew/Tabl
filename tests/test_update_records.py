import os
import pytest
from .context import update_records
from update_records import *

PATH_TEST_DB = "tests/test_databases/test_team_records.db"


def test_read_teams():
    teams = read_teams()
    assert len(teams) == 8


# def test_create_teams_table():
#     clear_table(PATH_TEST_DB)
#     create_teams_table(PATH_TEST_DB)
#     rows = get_records(PATH_TEST_DB)
#     assert len(rows) == 8
#     assert rows == [
#         ("1100", "David Unversity", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#         ("1200", "Jack University", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#         ("1300", "Aastha University A", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#         ("1301", "Aastha University B", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#         ("1400", "Sjoberg University A", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#         ("1401", "Sjoberg University B", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#         ("1500", "Nathan University", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#         ("1600", "Mia University", 0.0, 0.0, 0.0, 0.0, 0.0, "0", "0", "0", "0", "0"),
#     ]

def test_rank_teams():
    rank = rank_teams()
    assert rank == {'P1': '1301', 'D1': '1300', 'P2': '1600', 'D2': '1500', 'P3': '1401', 'D3': '1100', 'P4': '1200', 'D4': '1400'}