import sqlite3
import os
import sys
import random
from pairing import *


# ------------------------------------------------------------------------------------------------
#                                       Real Path Variables
# ------------------------------------------------------------------------------------------------

PATH_DB = "databases/team_records.db"
PATH_TEAMS = "teams.csv"
PATH_TEST_DB = "tests/test_databases/test_team_records.db"


# ------------------------------------------------------------------------------------------------
#                                     Set the database with info
# ------------------------------------------------------------------------------------------------


def read_teams(path=PATH_TEAMS):
    # open path, read and return a list of tuples (team number, team name) delimited by comma
    with open(path, "r") as f:
        read = f.read().splitlines()
    teams = []
    for line in read:
        teams.append(line.split(", "))
    return teams


def clear_table(path=PATH_DB):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM team_records""")
    conn.commit()
    conn.close()


def create_teams_table(path=PATH_DB):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS team_records
                    (team_number text, team_name text, Wins real, Losses real, CS real, OCS real, PD real, R1 text, R2 text, R3 text, R4 text, Side_Needed text)"""
    )

    # fill id and name
    teams = read_teams()
    for id, name in teams:
        cursor.execute(
            """INSERT INTO team_records VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)""",
            (id, name),
        )

    conn.commit()
    conn.close()


# database will look like this
"""
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| team_number | team_name            | Wins | Losses | CS | OCS | PD | R1 | R2 | R3 | R4 | Side_Needed |
+=============+======================+======+========+====+=====+====+====+====+====+====+=============+
| 1100        | David University     | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| 1200        | Jack University      | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| 1300        | Aastha University A  | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| 1301        | Aastha University B  | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| 1400        | Sjoberg University A | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| 1401        | Sjoberg University B | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| 1500        | Nathan University    | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
| 1600        | Mia University       | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  | 0           |
+-------------+----------------------+------+--------+----+-----+----+----+----+----+----+-------------+
"""


def get_records(path=PATH_DB):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM team_records""")
    rows = cursor.fetchall()
    conn.close()
    return rows


def print_table(path=PATH_DB):
    rows = get_records(path)
    for row in rows:
        print(row)


def read_ballot(path):
    # return winning team, point differential
    # open path and read
    with open(path, "r") as f:
        ballot = f.read().splitlines()
    # store first line as teams tuple
    teams = ballot[0].split(",")
    # store rest of lines as scores list of tuples
    scores = []
    for line in ballot[1:]:
        scores.append(line.split(","))
    p_total = 0
    d_total = 0
    for score in scores:
        p_total += int(score[0])
        d_total += int(score[1])
    # calculate point differential
    pd = abs(p_total - d_total)
    # return winning team and point differential
    if p_total > d_total:
        return (teams[0], teams[1], pd)
    elif d_total > p_total:
        return (teams[1], teams[0], pd)
    else:
        return (teams[0], teams[1], 0)


def get_round_updates(round_number: int):
    ballots_path = "ballots/round" + str(round_number)
    if not os.path.exists(ballots_path):
        return
    # go through each ballot and get the updates
    # return a list of tuples (team_number, win_loss)
    updates = []
    for ballot in os.listdir(ballots_path):
        updates.append(read_ballot(ballots_path + "/" + ballot))
    return updates


def get_pairings(path: str):
    with open(path, "r") as f:
        # store first line as teams tuple
        read = f.read().splitlines()
    # store rest of lines as scores list of tuples
    pairings = []
    for line in read:
        pairings.append(line.split(", "))
    return pairings


# ------------------------------------------------------------------------------------------------
#                                       Update Database
# ------------------------------------------------------------------------------------------------


def update_opponents(pairings_path, round_number: int) -> None:
    # connect to database
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()

    # get pairings
    pairings = get_pairings(pairings_path)
    print(pairings)
    """
    this should be based on the results from the pairings for a given round
    """
    for pair in pairings:
        team1 = pair[0]
        team2 = pair[1]

        if round_number == 1:
            # set R1 for team 1 as team 2
            cursor.execute(
                """UPDATE team_records SET R1 = ? WHERE team_number = ?""",
                (team2, team1),
            )
            # set R1 for team 2 as team 1
            cursor.execute(
                """UPDATE team_records SET R1 = ? WHERE team_number = ?""",
                (team1, team2),
            )
            # set sice needed for team1 as D
            cursor.execute(
                """UPDATE team_records SET Side_Needed = ? WHERE team_number = ?""",
                ("D", team1),
            )
            # set sice needed for team2 as p
            cursor.execute(
                """UPDATE team_records SET Side_Needed = ? WHERE team_number = ?""",
                ("P", team2),
            )

        elif round_number == 2:
            cursor.execute(
                """UPDATE team_records SET R2 = ? WHERE team_number = ?""",
                (team2, team1),
            )
            cursor.execute(
                """UPDATE team_records SET R2 = ? WHERE team_number = ?""",
                (team1, team2),
            )
            # set both teams' side_needed to N
            cursor.execute(
                """UPDATE team_records SET Side_Needed = ? WHERE team_number = ?""",
                ("N", team1),
            )
            cursor.execute(
                """UPDATE team_records SET Side_Needed = ? WHERE team_number = ?""",
                ("N", team2),
            )

        elif round_number == 3:
            cursor.execute(
                """UPDATE team_records SET R3 = ? WHERE team_number = ?""",
                (team2, team1),
            )
            cursor.execute(
                """UPDATE team_records SET R3 = ? WHERE team_number = ?""",
                (team1, team2),
            )
            # set sice needed for team1 as D
            cursor.execute(
                """UPDATE team_records SET Side_Needed = ? WHERE team_number = ?""",
                ("D", team1),
            )
            # set sice needed for team2 as p
            cursor.execute(
                """UPDATE team_records SET Side_Needed = ? WHERE team_number = ?""",
                ("P", team2),
            )
        elif round_number == 4:
            cursor.execute(
                """UPDATE team_records SET R4 = ? WHERE team_number = ?""",
                (team2, team1),
            )
            cursor.execute(
                """UPDATE team_records SET R4 = ? WHERE team_number = ?""",
                (team1, team2),
            )

    conn.commit()
    conn.close()


def update_records(round: int, path: str = PATH_DB) -> None:
    """
    this should be called at the conclusion of each round
    calls functions to:
    - update win-loss
    - update pd
    - update all round opponents
    """
    # connect to database
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # clear columns Wins, Losses, PD
    cursor.execute("""UPDATE team_records SET Wins = 0, Losses = 0, PD = 0""")
    conn.commit()

    for i in range(round, 0, -1):

        updates = get_round_updates(i)
        # go through each update
        for update in updates:
            # parse info
            winning_team = update[0]
            losing_team = update[1]
            pd = int(update[2])

            # update records
            if pd == 0:
                # add 0.5 to winning teams record at row[2]
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""",
                    (winning_team,),
                )
                row = cursor.fetchone()
                cursor.execute(
                    """UPDATE team_records SET Wins = ? WHERE team_number = ?""",
                    (row[2] + 0.5, winning_team),
                )
                # add 0.5 to winning teams record at row[3]
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""",
                    (winning_team,),
                )
                row = cursor.fetchone()
                cursor.execute(
                    """UPDATE team_records SET Losses = ? WHERE team_number = ?""",
                    (row[3] + 0.5, winning_team),
                )

                # add 0.5 to losing teams record at row[2]
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""",
                    (losing_team,),
                )
                row = cursor.fetchone()
                cursor.execute(
                    """UPDATE team_records SET Wins = ? WHERE team_number = ?""",
                    (row[2] + 0.5, losing_team),
                )
                # add 0.5 to losing teams record at row[3]
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""",
                    (losing_team,),
                )
                row = cursor.fetchone()
                cursor.execute(
                    """UPDATE team_records SET Losses = ? WHERE team_number = ?""",
                    (row[3] + 0.5, losing_team),
                )

            else:
                # winning team update record then pd
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""",
                    (winning_team,),
                )
                row = cursor.fetchone()
                cursor.execute(
                    """UPDATE team_records SET wins = ? WHERE team_number = ?""",
                    (row[2] + 1, winning_team),
                )

                cursor.execute(
                    """UPDATE team_records SET PD = ? WHERE team_number = ?""",
                    (row[6] + pd, winning_team),
                )

                # losing team update record then pd
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""",
                    (losing_team,),
                )
                row = cursor.fetchone()
                cursor.execute(
                    """UPDATE team_records SET losses = ? WHERE team_number = ?""",
                    (row[3] + 1, losing_team),
                )
                cursor.execute(
                    """UPDATE team_records SET PD = ? WHERE team_number = ?""",
                    (row[6] - pd, losing_team),
                )
    conn.commit()
    conn.close()


def update_cs(path=PATH_DB):
    # update the cs for each team
    # connect to database
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # get all teams
    cursor.execute("""SELECT * FROM team_records""")
    rows = cursor.fetchall()
    # go through each team
    for row in rows:
        # calculate cs
        cs = 0
        for i in range(7, 11):
            if row[i] != "0":
                op = row[i]
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""", (op,)
                )
                op_row = cursor.fetchone()
                cs += op_row[2]

        # update cs
        cursor.execute(
            """UPDATE team_records SET CS = ? WHERE team_number = ?""", (cs, row[0])
        )
    conn.commit()
    conn.close()


def update_ocs(path=PATH_DB):
    # update ocs for each team
    # connect to database
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # get all teams
    cursor.execute("""SELECT * FROM team_records""")
    rows = cursor.fetchall()
    # go through each team
    for row in rows:
        # calculate ocs
        ocs = 0
        for i in range(7, 11):
            if row[i] != "0":
                op = row[i]
                cursor.execute(
                    """SELECT * FROM team_records WHERE team_number = ?""", (op,)
                )
                op_row = cursor.fetchone()
                ocs += op_row[4]

        # update ocs
        cursor.execute(
            """UPDATE team_records SET ocs = ? WHERE team_number = ?""", (ocs, row[0])
        )
    conn.commit()
    conn.close()


# ------------------------------------------------------------------------------------------------
#                                       Ballot Stuff
# ------------------------------------------------------------------------------------------------


def generate_ballot(teams: list, path: str):
    # ***will generate a ballot with random scores and given team numbers
    team1 = teams[0]
    team2 = teams[1]

    for j in range(2):
        # generate 11 tuples of random scores between 5 and 10
        scores = []
        for i in range(14):
            scores.append((random.randint(5, 10), random.randint(5, 10)))
        # write to file
        filename = path + "/" + team1 + "_" + team2 + "_" + str(j) + ".csv"
        with open(filename, "w") as f:
            # write teams
            f.write(teams[0] + "," + teams[1] + "\n")
            # write scores
            for score in scores:
                f.write(str(score[0]) + "," + str(score[1]) + "\n")


def generate_round_ballots(round_number):
    # create folder for round
    folder = "round" + str(round_number)
    path = "ballots/" + folder
    if not os.path.exists(path):
        os.makedirs(path)

    # delete everything inside the folder
    for filename in os.listdir(path):
        os.remove(path + "/" + filename)

    # uses round 1 random pairing to generate ballots
    teams = read_teams()
    if round_number == 1:
        pairings = round_1_Pairings(teams)
    elif round_number == 2:
        pairings = round_2_Pairings(teams)
    elif round_number == 3:
        pairings = round_3_Pairings(teams)
    elif round_number == 4:
        pairings = round_4_Pairings(teams)

    print(pairings)
    for pairing in pairings:
        generate_ballot(pairing, path)


# ------------------------------------------------------------------------------------------------
#                                       Stuff For Pairings
# ------------------------------------------------------------------------------------------------
def rank_teams(path=PATH_DB, round_number=2):
    """
    for round 2: rankings are based on wins and pd
    """
    rankings = {}
    rows = get_records()

    condensed_teams = []
    for row in rows:
        condensed_teams.append([row[0], row[2], row[6], row[11]])

    # sort by wins first
    condensed_teams.sort(key=lambda x: x[1], reverse=True)

    # if two teams have same number of wins, sort them by pd
    for i in range(len(condensed_teams) - 1):
        if condensed_teams[i][1] == condensed_teams[i + 1][1]:
            if condensed_teams[i][2] < condensed_teams[i + 1][2]:
                condensed_teams[i], condensed_teams[i + 1] = (
                    condensed_teams[i + 1],
                    condensed_teams[i],
                )

    # if two teams have same number of wins and pd, sort them by higher team number
    for i in range(len(condensed_teams) - 1):
        if (
            condensed_teams[i][1] == condensed_teams[i + 1][1]
            and condensed_teams[i][2] == condensed_teams[i + 1][2]
        ):
            if int(condensed_teams[i][0]) < int(condensed_teams[i + 1][0]):
                condensed_teams[i], condensed_teams[i + 1] = (
                    condensed_teams[i + 1],
                    condensed_teams[i],
                )

    p_teams = []
    d_teams = []
    for team in condensed_teams:
        if team[3] == "P":
            p_teams.append(team)
        else:
            d_teams.append(team)

    # put p teams into rankings with key 'P' + str(rank)
    for i in range(len(p_teams)):
        rankings["P" + str(i + 1)] = p_teams[i][0]
        rankings["D" + str(i + 1)] = d_teams[i][0]

    return rankings


print(rank_teams())

# ------------------------------------------------------------------------------
#                               Misc/Testing Functions
# ------------------------------------------------------------------------------


def check_pd_single_ballot(ballot_path: str) -> None:
    # check pd for a single ballot
    # open file
    with open(ballot_path, "r") as f:
        # read teams
        teams = f.readline().split(",")
        team1 = teams[0]
        team2 = teams[1]
        # read scores
        scores = []
        for line in f:
            scores.append(line.split(","))
        # calculate pd
        pd = 0
        for score in scores:
            pd += int(score[0]) - int(score[1])
        # print results
        print(team1 + " pd: " + str(pd))


# check_pd_single_ballot('ballots/round1/1100_1301_0.csv')
