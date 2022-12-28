import random


def round_1_Pairings(teams):

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

def round_2_Pairings(pairings):
    pass

def round_3_Pairings(pairings):
    pass

def round_4_Pairings(pairings):
    pass

def round_4_Pairings_Nats(pairings):
    pass

def print_Pairings(pairings):
    for i, pairing in enumerate(pairings):
        print(f"Room {i+1}: {pairing[0]} vs {pairing[1]}")

