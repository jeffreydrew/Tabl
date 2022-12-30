import os
import pytest
from .context import update_records
from update_records import *

PATH_TEST_DB = "tests/test_databases/test_team_records.db"

def test_read_teams():
    teams = read_teams()
    assert len(teams) == 8

def test_create_teams_table():
    clear_table(PATH_TEST_DB)
    create_teams_table(PATH_TEST_DB)
    rows = get_records(PATH_TEST_DB)
    assert len(rows) == 8
