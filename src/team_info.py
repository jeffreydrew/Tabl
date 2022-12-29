class Round:
    def __init__(self, side, opponent_id, ballot1, ballot2) -> None:
        self.side = side
        self.opponent_id = opponent_id
        self.ballot1 = ballot1
        self.ballot2 = ballot2


class Team:
    def __init__(self, school_name, team_number) -> None:
        self.name = school_name
        self.id = team_number
        self.rounds = []
        self.record = 0
        self.running_cs = 0
        self.running_pd = 0
        self.rank = 0
