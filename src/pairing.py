import random


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


def round_2_Pairings(teams: list[list[str]]):
    pairings = []
    

    return pairings

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
