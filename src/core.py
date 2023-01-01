from update_records import *

clear_table()
create_teams_table()
# ------------------------------------------------------------------------------
#                                    Rounds
# ------------------------------------------------------------------------------
rounds = [1, 2, 3, 4]


def round(round, testing=False):
    if testing:
        generate_round_ballots(round)
    pairings_path = "pairings/round" + str(round) + ".csv"
    update_opponents(pairings_path, round)
    update_records(round)
    update_cs()
    update_ocs()


# ------------------------------------------------------------------------------
#                              Simulate Tournament
# ------------------------------------------------------------------------------
for i in rounds:
    round(i)
