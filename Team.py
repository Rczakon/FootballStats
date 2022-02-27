class Team:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.avg_goals_in_last5 = 0


    def calculate_avg_goals(self):
        total_goals_scored = []
        if len(self.matches) == 5:
            for match in self.matches:
                if match.team1 == self.name:
                    if (match.result[-1] != "-"):
                        total_goals_scored.append(int(match.result[0]))
                    else:
                        total_goals_scored.append(0)
                elif match.team2 == self.name:
                    if(match.result[-1] != "-"):
                        total_goals_scored.append(int(match.result[-1]))
                    else:
                        total_goals_scored.append(0)
                else:
                    print("Wrong match - incorrect teams found")
                    print("Searched: " + self.name)
                    print("Found: " + match.team1 + ", " + match.team2)
            if len(total_goals_scored) > 0:
                self.avg_goals_in_last5 = sum(total_goals_scored) / len(total_goals_scored)
            else:
                self.avg_goals_in_last5 = 0

# Required data:
# Goals in last 10 matches
# H2H in the current/last year
# League position
# Average goals in current season

# Red flags:
# - Guests
# - Less than 3 wins
#