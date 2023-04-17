from update_records import *
import time

clear_all_tables()
create_teams_table()
create_att_rankings_table()
create_wit_rankings_table()


# ------------------------------------------------------------------------------
#                                    Rounds
# ------------------------------------------------------------------------------
rounds = 4


def round(round, testing=False):
    if testing:
        generate_round_ballots(round)
    pairings_path = "pairings/round" + str(round) + ".csv"
    update_opponents(pairings_path, round)
    update_records(round)
    update_cs()
    update_ocs()
    # individual stuff
    update_individual_rankings(round)


# ------------------------------------------------------------------------------
#                              Simulate Tournament
# ------------------------------------------------------------------------------
print("Simulating UF Charity Tournament 2023...")
# start timer
start = time.time()

for i in range(1, rounds + 1):
    print("Processing ballots for round " + str(i) + "...")
    round(i)
    print("Round " + str(i) + " tabulation complete.")

get_winner()
# end timer
end = time.time()
print("Total tabulation time: " + str(end - start) + " seconds")
