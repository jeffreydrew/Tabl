from update_records import *


def round(round: int, testing: int = 0):
    if testing:
        generate_round_ballots(round)
    pairings_path = "pairings/round" + str(round) + ".csv"
    update_opponents(pairings_path, round)
    update_records(round)
    update_cs()
    update_ocs()


# ------------------------------------------------------------------------------
#                                Create Table
# ------------------------------------------------------------------------------

clear_table()
create_teams_table()


# ------------------------------------------------------------------------------
#                                   Round 1
# ------------------------------------------------------------------------------

round(1)
# ------------------------------------------------------------------------------
#                                   Round 2
# ------------------------------------------------------------------------------

#round(2)
# ------------------------------------------------------------------------------
#                                   Round 3
# ------------------------------------------------------------------------------

# round(3)
# ------------------------------------------------------------------------------
#                                   Round 4
# ------------------------------------------------------------------------------

# round(4)
