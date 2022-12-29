import os
import pytest
from update_records import *

PATH_TEST_DB = "tests/test_databases/test_team_records.db"

def test_create_teams_table():
    # create table
    create_teams_table(PATH_TEST_DB)
    # check if table exists
    assert os.path.exists(PATH_TEST_DB)

    assert len(get_records(PATH_TEST_DB)) == 8
     