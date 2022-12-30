from update_records import *

# ------------------------------------------------------------------------------
#                                Create Table
# ------------------------------------------------------------------------------
# this should only be done once at the beginning of the tournament
clear_table()
create_teams_table()


# ------------------------------------------------------------------------------
#                             Ballots for Round 1
# ------------------------------------------------------------------------------
# generate_round_ballots()

# ------------------------------------------------------------------------------
#                       Update Table with Round 1 Results
# ------------------------------------------------------------------------------
# get_round_results()
update_records()  # this updates wins, losses, and PD
update_cs()  # this updates CS
update_ocs()  # this updates OCS
# print table
