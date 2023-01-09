import random
import sqlite3

PATH_DB = "databases/team_records.db"

# ------------------------------------------------------------------------------------------------
#                                       Stuff For Pairings
# ------------------------------------------------------------------------------------------------
def rank_teams(round_number=2):
    """
    for round 2: rankings are based on wins and pd
    """

    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM team_records""")
    rows = cursor.fetchall()

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

    return condensed_teams


# rank_teams()


def check_impermissible(pair: list[str]):
    # impermissible if one of two things
    # 1. if they are from the same school
    # 2. if they have already played each other
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()

    # select team_name of pair[0]
    cursor.execute(
        """SELECT team_name FROM team_records WHERE team_id = ?""", (pair[0],)
    )
    team1 = cursor.fetchone()[0]
    # select team_name of pair[1]
    cursor.execute(
        """SELECT team_name FROM team_records WHERE team_id = ?""", (pair[1],)
    )
    team2 = cursor.fetchone()[0]
    if team1[:-2] == team2[:-2]:
        return True and print(
            "impermissible because of same school, "
            + team1
            + " and "
            + team2
            + ","
            + pair[0]
            + " and "
            + pair[1]
        )

    # select ROW of pair[0]
    cursor.execute("""SELECT * FROM team_records WHERE team_id = ?""", (pair[0],))
    row1 = cursor.fetchone()
    # select ROW of pair[1]
    cursor.execute("""SELECT * FROM team_records WHERE team_id = ?""", (pair[1],))
    row2 = cursor.fetchone()
    team1_ops = row1[7:11]
    team2_ops = row2[7:11]
    if pair[1] in team1_ops:
        return True and print(
            "impermissible because of previous match between "
            + pair[0]
            + " and "
            + pair[1]
        )
    if pair[0] in team2_ops:
        return True and print(
            "impermissible because of previous match between "
            + pair[1]
            + " and "
            + pair[0]
        )

    return False


# ------------------------------------------------------------------------------------------------
#                                           Pairings
# ------------------------------------------------------------------------------------------------


def round_1_Pairings(teams: list[list[str]]):
    pairings = []
    ids = []
    copy = {}

    for id, name in teams:
        ids.append(id)
        copy[id] = name

    for i in range(len(teams) // 2):
        team1 = random.choice(ids)
        team2 = random.choice(ids)
        while team1 == team2:
            team2 = random.choice(ids)
        # the only applicable impermissibility condition is if the teams are from the same school because no rounds have been played yet

        # if they are from the same school:
        # As per AMTA Tab manual page 16, teams from the same school cannot be paired. It they are, the second
        # team is returned to the pool and a new team is drawn. If this is the last pairing, the second team
        # is switched with the last drawn team.
        if copy[team1][:-2] == copy[team2][:-2]:
            # if not last pairing
            if i != len(teams) // 2 - 1:
                valid_ids = ids.copy()
                valid_ids.remove(team1)
                valid_ids.remove(team2)
                team2 = random.choice(valid_ids)
                valid_ids.clear()
                pairings.append([team1, team2])

            # if last
            else:
                temp = pairings.pop(-1)
                pulled_team = temp[1]
                temp[1] = team2
                pairings.append(temp)
                pairings.append([team1, pulled_team])

        else:
            pairings.append([team1, team2])
        ids.remove(team1)
        ids.remove(team2)

    # write pairings to corresponding round pairing file
    filename = "pairings/round1.csv"
    with open(filename, "w") as f:
        # write pairings
        for pair in pairings:
            f.write(pair[0] + ", " + pair[1] + "\n")

    return pairings


def round_2_Pairings():
    pairings = []
    rankings = {}
    condensed_teams = rank_teams(2)

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

    # print(len(rankings))
    # this is going to need a change to account for teams hitting each other before
    for i in range(1, len(rankings) // 2 + 1):
        pairings.append([rankings["P" + str(i)], rankings["D" + str(i)]])

    # check all pairings for impermissibility
    for pair in pairings:
        if check_impermissible(pair):
            # make an inplace change to pairings list to fix impermissible pairing
            return

    # write pairings to corresponding round pairing file
    filename = "pairings/round2.csv"
    with open(filename, "w") as f:
        # write pairings
        for pair in pairings:
            f.write(pair[0] + ", " + pair[1] + "\n")

    return pairings


# round_2_Pairings()


def round_3_Pairings():
    pairings = []
    rankings = {}

    condensed_teams = rank_teams(3)

    # for team in condensed_teams:
    #     print(team[0])

    for i in range(1, len(condensed_teams) + 1):
        rankings["R" + str(i)] = condensed_teams[i - 1][0]

    switch = False
    for i in range(1, len(rankings) + 1, 2):
        # this creates the snaking pattern for team rankings as outlined in AMTA TAB MANUAL page 18
        if not switch:
            pairings.append([rankings["R" + str(i)], rankings["R" + str(i + 1)]])
            switch = not switch
        else:
            pairings.append([rankings["R" + str(i + 1)], rankings["R" + str(i)]])
            switch = not switch

    # write pairings to corresponding round pairing file
    filename = "pairings/round3.csv"
    with open(filename, "w") as f:
        # write pairings
        for pair in pairings:
            f.write(pair[0] + ", " + pair[1] + "\n")

    return pairings


# print(round_3_Pairings())


def round_4_Pairings(teams: list[list[str]]):
    pairings = []
    ids = []
    copy = {}

    for id, name in teams:
        ids.append(id)
        copy[id] = name

    for i in range(len(teams) // 2):
        team1 = random.choice(ids)
        team2 = random.choice(ids)
        while team1 == team2:
            team2 = random.choice(ids)
        # if they are from the same school:
        # As per AMTA Tab manual page 16, teams from the same school cannot be paired. It they are, the second
        # team is returned to the pool and a new team is drawn. If this is the last pairing, the second team
        # is switched with the last drawn team.
        if copy[team1][:-2] == copy[team2][:-2]:
            # if not last pairing
            if i != len(teams) // 2 - 1:
                valid_ids = ids.copy()
                valid_ids.remove(team1)
                valid_ids.remove(team2)
                team2 = random.choice(valid_ids)
                valid_ids.clear()
                pairings.append([team1, team2])

            # if last
            else:
                temp = pairings.pop(-1)
                pulled_team = temp[1]
                temp[1] = team2
                pairings.append(temp)
                pairings.append([team1, pulled_team])

        else:
            pairings.append([team1, team2])
        ids.remove(team1)
        ids.remove(team2)

    # write pairings to corresponding round pairing file
    filename = "pairings/round4.csv"
    with open(filename, "w") as f:
        # write pairings
        for pair in pairings:
            f.write(pair[0] + ", " + pair[1] + "\n")

    return pairings


def round_4_Pairings_Nats():
    pairings = []
    rankings = {}
    condensed_teams = rank_teams(2)

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

    # print(len(rankings))
    # this is going to need a change to account for teams hitting each other before
    for i in range(1, len(rankings) // 2 + 1):
        pairings.append([rankings["P" + str(i)], rankings["D" + str(i)]])

    # write pairings to corresponding round pairing file
    filename = "pairings/round4.csv"
    with open(filename, "w") as f:
        # write pairings
        for pair in pairings:
            f.write(pair[0] + ", " + pair[1] + "\n")

    return pairings


def print_Pairings(pairings):
    for i, pairing in enumerate(pairings):
        print(f"Room {i+1}: {pairing[0]} vs {pairing[1]}")
