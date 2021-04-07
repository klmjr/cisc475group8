import z3
from itertools import product 
# Definition of Constants 
""" 
Since z3 handles integers better than strings, we will define all of the string constants as integers
""" 
## Teams 

## Divisions 

## No Team: For different iterations of the solver, it may be best to let the solver not place a team. In that case we reserve -1 to be that teams number. 

TEAM = -1 

# PLAN: 
""" 
Make solvers for unrelated scenarios, combine results together to create final schedule. 
Solver 1: 
The Saturday meets 

Solver 2: 

""" 
RED = 0 
WHITE = 1 
BLUE = 2 
def Team(): 
    def __init__(self, number, division, wins, losses):
        pass


# Solve Saturday meets problem



# Generates the array of opponent variables and sets up a solver object with 
#    basic schedule constraints: 
#       * Commutativity of opponents, i.e. Team 0 is playing Team 1 and Team 1 is playing team 0 
#       * Opposite home and away for opponents, (Team0 AND 1) XOR (Team1 AND 1) == 1. 
#       * Each opponent is distinct 
#       * Other misc constraints: a team should not play themselves, a team should be a valid team etc. 
# The variable for each opponent is a packed BitVector. In order to get the most out of the variables,
#    the bits are packed like TeamNum|Home, where home is 1 or 0. To extract the info from the vec the 
#    operations are: 
#       * Team: Var >> 1 (Bit-Shift right) 
#       * Home?: Var & 1 (Bit-wise AND with 1) 
def generate_variables(num_teams, num_games): 
    # Each row in the 2 x 2 array is the list of opponents for the team the rows correspond to 
    games = [[z3.BitVec(f"Team_{i}_Game_{j}", 32) for j in range(1, num_games + 1)] for i in range(num_teams)]
    
    s = z3.Solver() 

    # Each row must have a valid team 
    for team in range(num_teams):
        opponents = games[team] # Get the opponents for the team
        for opp in opponents: 
            s.add(z3.And((opp >> 1) < num_teams, (opp >> 1) >= 0)) # Team in a valid range 
            s.add((opp >> 1) != team) # Team can't play themselves 
    
    # Handle Distinct opponents 
    for team_opps in games: 
        opponent_teams = [] 
        for opp in team_opps: 
            opponent_teams.append(opp >> 1) 
        s.add(z3.Distinct(opponent_teams)) 
    # Commutativity of opponents and home and away basics 
    # This code will look janky, but z3 variables can't be used as python list indices
    # so forgive me 
    for team1, team2 in product(range(num_teams), repeat=2): 
        if (team1 == team2): 
            continue 
        for game in range(num_games): 
            opposing_team1 = games[team1][game] >> 1
            opposing_team2 = games[team2][game] >> 1 
            team1_home = games[team1][game] & 1 
            team2_home = games[team2][game] & 1 
            if_true = z3.And(opposing_team2 == team1, (team1_home ^ team2_home) == 1  )
            s.add(z3.If(opposing_team1 == team2, if_true, True)) 

    if (s.check() == z3.sat): 
        print("we're cooling") 
    return s, games

def print_game_model(solver, games, num_games, num_teams): 
    if (solver.check() != z3.sat): 
        print("Houston... we have a problem") 
        return -1 
    model = solver.model() 
    solution_games = [[model[games[team][game]].as_long() for game in range(num_games)] for team in range(num_teams)] 

    line1 = " "*10 
    for i in range(num_games): 
        line1 += f"Game{i}" + " "*8 
    print(line1) 
    for team in range(num_teams): 
        line = f"Team{team}" + " "*8 
        for game in range(num_games): 
            sol_result = solution_games[team][game] 
            home = sol_result & 1 
            opposer = sol_result >> 1 
            line += f"{opposer}" 
            if (home == 1): 
                line += "H" 
            else: 
                line += "A" 
            line += " "*8 
        print(line) 

def main(): 
    # There are 8 meets and 20 teams 
    solver, games = generate_variables(20, 8) 
    print_game_model(solver, games, 8, 20) 
if __name__ == "__main__": 
    main() 
