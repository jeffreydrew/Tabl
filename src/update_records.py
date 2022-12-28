import sqlite3
import os
import math
import random
from pairing import *

# ------------------------------------------------------------------------------------------------
#                                       Global Variables
# ------------------------------------------------------------------------------------------------

PATH_DB = "databases/team_records.db"
PATH_TEAMS = "src/teams.csv"


def read_teams(path=PATH_TEAMS):
    with open(path, "r") as f:
        teams = f.read().splitlines()
    return teams


def create_teams_table(path=PATH_DB):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS team_records
                    (team_number text, wins integer, losses integer)"""
    )
    teams = read_teams()
    for team in teams:
        cursor.execute("""INSERT INTO team_records VALUES (?, 0, 0)""", (team,))
    conn.commit()
    conn.close()


def create_empty_table(path="databases/team_records.db"):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS team_records
                    (team_number text, wins integer, losses integer)"""
    )
    # insert 6 teams with 0 wins and 0 losses
    cursor.execute("""INSERT INTO team_records VALUES (1, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (2, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (3, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (4, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (5, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (6, 0, 0)""")

    conn.commit()
    conn.close()


def update_records(team_number, win_loss):
    conn = sqlite3.connect("databases/team_records.db")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM team_records WHERE team_number = ?""", (team_number,)
    )
    row = cursor.fetchone()
    if win_loss == "win":
        cursor.execute(
            """UPDATE team_records SET wins = ? WHERE team_number = ?""",
            (row[1] + 1, team_number),
        )
    elif win_loss == "loss":
        cursor.execute(
            """UPDATE team_records SET losses = ? WHERE team_number = ?""",
            (row[2] + 1, team_number),
        )

    conn.commit()
    conn.close()


def clear_table(path=PATH_DB):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM team_records""")
    conn.commit()
    conn.close()


def get_records(path=PATH_DB):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM team_records""")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------------------------------------------
#                                       Ballot Stuff
# ------------------------------------------------------------------------------------------------


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
        return teams[0], pd
    elif d_total > p_total:
        return teams[1], pd
    else:
        return "0000", 0


def generate_random_ballot(number_of_ballots=1):
    # ***will generate a ballot with random scores and random team numbers
    teams = read_teams()
    team1 = random.choice(teams)
    team2 = random.choice(teams)
    while team2 == team1:
        team2 = random.choice(teams)
    # generate 11 tuples of random scores between 5 and 10
    scores = []
    for i in range(11):
        scores.append((random.randint(5, 10), random.randint(5, 10)))
    # write to file
    with open("ballots/ballot.csv", "w") as f:
        # write teams
        f.write(team1 + "," + team2 + "\n")
        # write scores
        for score in scores:
            f.write(str(score[0]) + "," + str(score[1]) + "\n")


def generate_ballot(teams, path):
    # ***will generate a ballot with random scores and given team numbers
    team1 = teams[0]
    team2 = teams[1]
    # generate 11 tuples of random scores between 5 and 10
    scores = []
    for i in range(11):
        scores.append((random.randint(5, 10), random.randint(5, 10)))
    # write to file
    filename = path + "/" + team1 + "_" + team2 + ".csv"
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
    pairings = round_1_Pairings(teams)
    for pairing in pairings:
        generate_ballot(pairing, path)


generate_round_ballots(1)


def update_team_records():
    # files = []
    # for root, dirs, files in os.walk("ballots"):
    #     files.append(files)
    # return files[:-1]
    # ***will read through all ballots and update the database after clearing it
    for root, dirs, files in os.walk("ballots"):
        ballot = read_ballot(os.path.join(root, files[0]))
