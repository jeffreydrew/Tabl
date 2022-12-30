import sqlite3
import os
import random
from pairing import *

# ------------------------------------------------------------------------------------------------
#                                       Real Path Variables
# ------------------------------------------------------------------------------------------------

PATH_DB = "databases/team_records.db"
PATH_TEAMS = "teams.csv"


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
                    (team_number text, team_name text, Wins real, Losses real, CS real, OCS real, PD real, R1 text, R2 text, R3 text, R4 text)"""
    )

    # fill id and name
    teams = read_teams()
    for id, name in teams:
        cursor.execute(
            """INSERT INTO team_records VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0)""",
            (id, name),
        )

    conn.commit()
    conn.close()


# database will look like this
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | team_number | team_name            | Wins | Losses | CS | OCS | PD | R1 | R2 | R3 | R4 |
# +=============+======================+======+========+====+=====+====+====+====+====+====+
# | 1100        | David University     | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | 1200        | Jack University      | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | 1300        | Aastha University A  | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | 1301        | Aastha University B  | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | 1400        | Sjoberg University A | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | 1401        | Sjoberg University B | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | 1500        | Nathan University    | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+
# | 1600        | Mia University       | 0    | 0      | 0  | 0   | 0  | 0  | 0  | 0  | 0  |
# +-------------+----------------------+------+--------+----+-----+----+----+----+----+----+


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


def get_round_updates(ballots_path="ballots/round1"):
    # go through each ballot and get the updates
    # return a list of tuples (team_number, win_loss)
    updates = []
    for ballot in os.listdir(ballots_path):
        updates.append(read_ballot(ballots_path + "/" + ballot))
    return updates


def update_records(path=PATH_DB):
    '''
    Updates the wins, losses, and point differential for each team, as well as the round 1 opponent
    '''

    updates = get_round_updates()
    # connect to database
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # go through each update
    for update in updates:
        # parse info
        winning_team = update[0]
        losing_team = update[1]
        pd = int(update[2])

        #set oppenent for winning team to losing team
        cursor.execute(
            """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
        )
        row = cursor.fetchone()
        cursor.execute(
            """UPDATE team_records SET R1 = ? WHERE team_number = ?""",
            (losing_team, winning_team),
        )
        #set oppenent for losing team to winning team
        cursor.execute(
            """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
        )
        row = cursor.fetchone()
        cursor.execute(
            """UPDATE team_records SET R1 = ? WHERE team_number = ?""",
            (winning_team, losing_team),
        )

        # update records
        if pd == 0:
            #add 0.5 to winning teams record at row[2]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Wins = ? WHERE team_number = ?""",
                (row[2] + 0.5, winning_team),
            )
            # add 0.5 to winning teams record at row[3]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Losses = ? WHERE team_number = ?""",
                (row[3] + 0.5, winning_team),
            )

            
            # add 0.5 to losing teams record at row[2]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Wins = ? WHERE team_number = ?""",
                (row[2] + 0.5, losing_team),
            )
            # add 0.5 to losing teams record at row[3]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Losses = ? WHERE team_number = ?""",
                (row[3] + 0.5, losing_team),
            )

        else:
            # winning team update record then pd
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
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
                """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
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
        for i in range(7,11):
            if row[i] != '0':
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
    #update ocs for each team
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
        for i in range(7,11):
            if row[i] != '0':
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


def generate_round_ballots(round_number=1):
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
    print(pairings)
    for pairing in pairings:
        generate_ballot(pairing, path)
