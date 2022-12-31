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
    rankings = {}

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
    rankings = rank_teams(2)

    # for i in half the length of the rankings list:
    for i in range(1, len(rankings) // 2 + 1):
        pairings.append([rankings["P" + str(i)], rankings["D" + str(i)]])

    return pairings


# print round 2 pairings
print(round_2_Pairings())


def round_3_Pairings(teams: list[list[str]]):
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
    filename = "pairings/round3.csv"
    with open(filename, "w") as f:
        # write pairings
        for pair in pairings:
            f.write(pair[0] + ", " + pair[1] + "\n")

    return pairings


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


def round_4_Pairings_Nats(teams: list[list[str]]):
    pass


def print_Pairings(pairings):
    for i, pairing in enumerate(pairings):
        print(f"Room {i+1}: {pairing[0]} vs {pairing[1]}")
