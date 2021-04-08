import z3
from itertools import product 
from swim_data import wins_and_losses 
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
class Helper(): 
    def __init__(self, solver, games, wins_losses, red, white, blue):
        self.solver = solver
        self.games = games
        self.wins_losses = wins_losses 
        self.red = red 
        self.white = white 
        self.blue = blue
        self.red_pairings = [] 
        self.white_pairings = [] 
        self.blue_pairings = [] 
        red_div = sorted(wins_losses[red[0]:red[1] + 1], key=lambda team: team['ratio'][0])  
        blue_div = sorted(wins_losses[blue[0]:blue[1] + 1], key=lambda team: team['ratio'][0]) 
        white_div = sorted(wins_losses[white[0]:white[1] + 1], key=lambda team: team['ratio'][0]) 
        for division in [(self.red_pairings, red_div), (self.white_pairings, white_div), (self.blue_pairings, blue_div)]: 
            pairings, div = division
            for i in range(0,len(div), 2):
                print(i) 
                if (i + 1 > len(div) - 1 ): 
                   opp = -1 
                else: 
                    opp = div[::-1][i + 1]['team'] 
                pairings.append((div[::-1][i]['team'], opp)) 
        



def find_competitors(win_loss): 
    sorted_teams = sorted(win_loss, key=lambda team: team['ratio'][0]) 
    print(sorted_teams) 
# Solve Saturday meets problem
# Find most competitive teams and pair them for final game
# Make sure there are the correct number of Saturday meets based on number of Saturdays
# 

def saturday_meets(solver, games, win_loss): 
    pairings = find_competitors(win_loss) 


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
            s.add(z3.And((opp >> 1) < num_teams, (opp >> 1) >= -1 )) # Team in a valid range 
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
        line = f"Team{team}" 
        for game in range(num_games): 
            line = line.ljust(13*(game + 1), " ")  
            sol_result = solution_games[team][game] 
            home = sol_result & 1 
            opposer = sol_result >> 1 
            line += f"{opposer}" 
            if (home == 1): 
                line += "H" 
            else: 
                line += "A" 
        print(line) 

def main(): 
    # There are 8 meets and 20 teams 
    solver, games = generate_variables(20, 8) 
    x = Helper(solver,games,wins_and_losses,(0, 6), (7, 12), (13, 19)) 
    print(x.red_pairings) 
    print_game_model(solver, games, 8, 20) 
if __name__ == "__main__": 
    main() 
