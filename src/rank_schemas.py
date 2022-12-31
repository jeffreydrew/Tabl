PATH_DB = "databases/team_records.db"
from update_records import get_records

# ------------------------------------------------------------------------------------------------
#                                       Stuff For Pairings
# ------------------------------------------------------------------------------------------------
def rank_teams(round_number=2):
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
