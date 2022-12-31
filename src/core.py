from update_records import *

# ------------------------------------------------------------------------------
#                                Create Table
# ------------------------------------------------------------------------------

clear_table()
create_teams_table()


# ------------------------------------------------------------------------------
#                                   Round 1
# ------------------------------------------------------------------------------

#generate_round_ballots(1)
update_opponents("pairings/round1.csv", 1)
update_records(1)
update_cs()
update_ocs()
# ------------------------------------------------------------------------------
#                                   Round 2
# ------------------------------------------------------------------------------

#generate_round_ballots(2)
update_opponents("pairings/round2.csv", 2)
update_records(2)
update_cs()
update_ocs()
# ------------------------------------------------------------------------------
#                                   Round 3
# ------------------------------------------------------------------------------

#generate_round_ballots(3)
update_opponents("pairings/round3.csv", 3)
update_records(3)
update_cs()
update_ocs()
# ------------------------------------------------------------------------------
#                                   Round 4
# ------------------------------------------------------------------------------

#generate_round_ballots(4)
update_opponents("pairings/round4.csv", 4)
update_records(4)
update_cs()
update_ocs()