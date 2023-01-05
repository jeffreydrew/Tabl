from update_records import *
import time

clear_table()
# clear_table("databases/individual_rankings.db")
create_teams_table()
create_individual_rankings_table()
# ------------------------------------------------------------------------------
#                                    Rounds
# ------------------------------------------------------------------------------
rounds = 4


def round(round, testing=True):
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
# start timer
start = time.time()

for i in range(1, rounds + 1):
    round(i)

get_winner()
# end timer
end = time.time()
print("Time elapsed: " + str(end - start) + " seconds")
