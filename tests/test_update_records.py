import os
import pytest
from .context import update_records
from update_records import *

def test_read_teams():
    teams = read_teams()
    assert len(teams) == 8

