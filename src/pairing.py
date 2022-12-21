import random

teams = [
    "1100",
    "1200",
    "1300",
    "1301",
    "1400",
    "1500",
    "1600",
    "1700",
    "1800",
    "1900",
]


def initialPairings(teams):

    random.shuffle(teams)
    pairings = []  # list of tuples (team1, team2)

    for i in range(0, len(teams), 2):
        team1 = random.choice(teams)
        team2 = random.choice([team for team in teams if team != team1])

        # As per AMTA Tab manual page 16, teams from the same school cannot be paired. It they are, the second
        # team is returned to the pool and a new team is drawn. If this is the last pairing, the second team
        # is switched with the last drawn team.
        if team1[:2] == team2[:2]:
            # if not the last pairing, return the second team to the pool and draw a new one
            newTeam2 = random.choice(
                [team for team in teams if team != team1 and team != team2]
            )
            pairings.append((team1, newTeam2))

            # if this is the last pairing, switch the second team with the last drawn team
            temp = pairings[-1][1]
            pairings[-1][1] = team2
            pairings.append((team1, temp))
        else:
            pairings.append((team1, team2))

        teams.remove(team1)
        teams.remove(team2)

    return pairings

def round2Pairings(pairings):
    pass

def round3Pairings(pairings):
    pass

def round4Pairings(pairings):
    pass

def round4Pairings_Nats(pairings):
    pass

def printPairings(pairings):
    for i, pairing in enumerate(pairings):
        print(f"Room {i+1}: {pairing[0]} vs {pairing[1]}")


round1 = initialPairings(teams)
printPairings(round1)
