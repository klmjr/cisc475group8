import z3
from itertools import product 
from swim_data import wins_and_losses, teams as teams_list, changed 
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

class Blue():
    
    def gen_final_pairings(self, data): 
        # Make deep copies of sorted win-loss ratio of prior years 
        blue = [x for x in data.blue_div] 
        white = [x for x in data.white_div] 
        pairings = []  
        
        best_of_blue = blue[0]['team']
        worst_of_white = white[-1]['team'] 
        """  
        i = 0 
        while (white[-1 - i]['team'] ==  data.changed_division['red_to_white']): 
            i++
            worst_of_white = white[-1-i]['team']
        """ 
        pairings.append((best_of_blue, worst_of_white)) 

        del blue[0] 

        for i in range(0, len(blue), 2): 
            pairings.append((blue[i]['team'], blue[i + 1]['team'])) 

        for pairing in pairings: 
            team1, team2 = pairing 

            data.solver.add(getTeam(data.games[team1][-1]) == team2) 

         
    def intradivision_games(self, data):
        start_blue, end_blue = data.blue_indices 
        start_white, end_white = data.white_indices
        for weeks in range(1, data.num_games - 1): 
            count_intra = 0 
            count_inter = 0 
            for team in range(start_blue, end_blue + 1): 
                intra_cond = z3.And(getTeam(data.games[team][weeks]) <= end_blue, getTeam(data.games[team][weeks]) >= start_blue ) 
                inter_cond = z3.And(getTeam(data.games[team][weeks]) <= end_white, getTeam(data.games[team][weeks]) >= start_white) 
                count_intra += z3.If(intra_cond, 1, 0) 
                count_inter += z3.If(inter_cond, 1, 0) 
            data.solver.add(count_intra == end_blue - start_blue)
            data.solver.add(count_inter == 1) 
    def isCrossover(self,team1, team2, data): 
        start, end = data.blue_indices 
        first_cond = (team1 in range(start, end + 1) and not(team2 in range(start, end + 1))) 
        second_cond = (team2 in range(start, end + 1) and not(team1 in range(start, end + 1))) 
        return first_cond or second_cond
        
        

class Red(): 
    def gen_final_pairings(self, data): 
        # Make deep copies of win-loss ratios 
        red = [x for x in data.red_div] 
        white = [x for x in data.white_div] 

        changed_index = 0 

        for i in range(len(red)): 
            if (red[i]['team'] == data.changed_division['white_to_red']): 
                changed_index = i 
                break 
        pairings = [] 
        
        best_of_white = white[0]['team']

        pairings.append((red[changed_index]['team'], best_of_white)) 

        del red[changed_index] 

        for i in range(0, len(red), 2): 
            pairings.append((red[i]['team'], red[i + 1]['team'])) 

        for pairing in pairings: 
            team1, team2 = pairing 
            data.solver.add(getTeam(data.games[team1][-1]) == team2) 
    def intradivision_games(self, data): 
        start_red, end_red = data.red_indices 
        start_white, end_white = data.white_indices
        for weeks in range(1, data.num_games - 1): 
            count_intra = 0 
            count_inter = 0 
            for team in range(start_red, end_red + 1): 
                intra_cond = z3.And(getTeam(data.games[team][weeks]) <= end_red, getTeam(data.games[team][weeks]) >= start_red ) 
                inter_cond = z3.And(getTeam(data.games[team][weeks]) <= end_white, getTeam(data.games[team][weeks]) >= start_white) 
                count_intra += z3.If(intra_cond, 1, 0) 
                count_inter += z3.If(inter_cond, 1, 0) 
            data.solver.add(count_intra == end_red - start_red)
            data.solver.add(count_inter == 1) 
    def isCrossover(self, team1, team2, data):  
        start, end = data.red_indices 
        first_cond = (team1 in range(start, end + 1) and not(team2 in range(start, end + 1))) 
        second_cond = (team2 in range(start, end + 1) and not(team1 in range(start, end + 1))) 
        return first_cond or second_cond

class White():
    def gen_final_pairings(self, data): 
        white = [x for x in data.white_div] 

        del white[0] 
        del white[-1]
        
        pairings = [] 
        for i in range(0, len(white), 2): 
           pairings.append((white[i]['team'], white[i + 1]['team'])) 

        for pairing in pairings: 
            team1, team2 = pairing 
            data.solver.add(getTeam(data.games[team1][-1]) == team2) 
    def intradivision_games(self, data): 
    
        start_white, end_white = data.white_indices
        
        for weeks in range(1, data.num_games - 1): 
            count_intra = 0 
            for team in range(start_white, end_white + 1): 
                intra_cond = z3.And(getTeam(data.games[team][weeks]) <= end_white, getTeam(data.games[team][weeks]) >= start_white ) 
                count_intra += z3.If(intra_cond, 1, 0) 
            data.solver.add(count_intra == end_white - start_white - 1)
    def isCrossover(self,team1, team2, data):  
        start, end = data.white_indices 
        first_cond = (team1 in range(start, end + 1) and not(team2 in range(start, end + 1))) 
        second_cond = (team2 in range(start, end + 1) and not(team1 in range(start, end + 1))) 
        return first_cond or second_cond

class Data(): 
    def __init__(self, num_games, num_teams, wins_losses, red, white, blue, changed, saturdays):
        self.num_games = num_games 
        self.num_teams = num_teams
        self.wins_losses = wins_losses 
        self.red_indices = red 
        self.white_indices = white 
        self.blue_indices = blue
        self.changed_division = changed 
        self.saturdays = saturdays
        self.red_div = sorted(wins_losses[red[0]:red[1] + 1], key=lambda team: team['ratio'][0])[::-1] 
        self.blue_div = sorted(wins_losses[blue[0]:blue[1] + 1], key=lambda team: team['ratio'][0])[::-1] 
        self.white_div = sorted(wins_losses[white[0]:white[1] + 1], key=lambda team: team['ratio'][0])[::-1]  
        self.divisions = [Red(), White(), Blue()] 
        self.generate_variables(self.num_games, self.num_teams) 
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
    def generate_variables(self, num_games, num_teams): 
        # Each row in the 2 x 2 array is the list of opponents for the team the rows correspond to 
        games = [[z3.BitVec(f"Team_{i}_Game_{j}", 32) for j in range(1, num_games + 1)] for i in range(num_teams)]
        
        s = z3.Solver() 

        # Each row must have a valid team 
        for team in range(num_teams):
            opponents = games[team] # Get the opponents for the team
            for opp in opponents: 
                s.add(z3.And(getTeam(opp) < num_teams, getTeam(opp) >= -1 )) # Team in a valid range 
                s.add((opp >> 1) != team) # Team can't play themselves 
        
        # Handle Distinct opponents 
        for team_opps in games: 
            opponent_teams = [] 
            count = 0
            for opp in team_opps: 
                opponent_teams.append(getTeam(opp)) 
                count += z3.If(getTeam(opp)== -1, 1, 0 ) 
            s.add(z3.Or(z3.Distinct(opponent_teams), count > 1 ))  
        # Commutativity of opponents and home and away basics 
        # This code will look janky, but z3 variables can't be used as python list indices
        # so forgive me 
        for team1, team2 in product(range(num_teams), repeat=2): 
            if (team1 == team2): 
                continue 
            for game in range(num_games): 
                opposing_team1 = getTeam(games[team1][game])
                opposing_team2 = getTeam(games[team2][game] )
                team1_home = getHome(games[team1][game])
                team2_home = getHome(games[team2][game]) 
                if_true = z3.And(opposing_team2 == team1, (team1_home ^ team2_home) == 1  )
                s.add(z3.If(opposing_team1 == team2, if_true, True)) 
        for team in games: 
            sums = 0 
            for game in team: 
                sums += z3.If(getHome(game) == 1, 1, 0) 
            s.add(sums == 4) 

        self.solver = s 
        self.games = games  
class TeamGenerator(): 
    def __init__(self, data):
        self.data = data
        self.saturday_meets()
          
        self.intradivision_games()
        self.first_saturday_crossovers()  
    def saturday_meets(self): 
        # Schedule the last saturday 
        for division in self.data.divisions: 
            division.gen_final_pairings(self.data) 

        # Make sure the number of saturday homegames is correct # TODO update this to include the variability that can occur depending on number of Saturday games etc.
        for team in range(len(self.data.games)): 
            opponents = self.data.games[team] 
            count = 0 
            for day in self.data.saturdays: 
                count += z3.If(getHome(opponents[day]) == 1, 1, 0) 
            self.data.solver.add(z3.Or(count == 2, count == 3)) 
        
                
        pass 
    def intradivision_games(self): 
        for division in self.data.divisions: 
            division.intradivision_games(self.data) 
    def first_saturday_crossovers(self): 
         
        for team in range(len(self.data.games)): 
            game = self.data.games[team][0] # The first game in the season 
            if (team in range(self.data.red_indices[0], self.data.red_indices[1] + 1)): 
                opponent = getTeam(game)
                self.data.solver.add(z3.And(opponent > self.data.red_indices[1], opponent <= self.data.blue_indices[1]))
            elif (team in range(self.data.blue_indices[0], self.data.blue_indices[1] + 1)): 
                opponent = getTeam(game)
                self.data.solver.add(z3.And(opponent >= self.data.red_indices[0], opponent <= self.data.white_indices[1]))
             
            else: 
                # Team is a white team 
                opponent = getTeam(game) 
                blue_opp = z3.And(opponent <= self.data.blue_indices[1], opponent >= self.data.blue_indices[0])
                red_opp = z3.And(opponent <= self.data.red_indices[1], opponent >= self.data.red_indices[0])
                self.data.solver.add(z3.Or(blue_opp, red_opp)) 
          

#Get home 
# Input: a Symbolic Variable or an Int 
# Output: Whether the team is home or way
def getHome(team): 
    return team & 0x1 

#getTeam
# Input: a Symbolic Variable or an Int 
# Output: the team corresponding to the Input 
def getTeam(team): 
    return team >> 1 


def print_game_model(data): 
    print("here1") 
    if (data.solver.check() != z3.sat): 
        print("Houston... we have a problem") 
        return -1
    print("here2") 
    model = data.solver.model() 
    solution_games = [[model[data.games[team][game]].as_long() for game in range(data.num_games)] for team in range(data.num_teams)] 
    
    line1 = " "*12 
    for i in range(data.num_games): 
        line1 += f"Game{i}" + " "*8 
    print(line1) 
    for team in range(data.num_teams):
        if (team != 2147483647): 
            line = f"{team} {teams_list[team][:9]}" 
        else: 
            line = f"Team{team}"
        home_count = 0 
        saturdays = [0, 2, 4,5,7] 
        saturday_home_count = 0 
        for game in range(data.num_games): 
            line = line.ljust(13*(game + 1), " ")  
            sol_result = solution_games[team][game] 
            home = sol_result & 1 
            opposer = sol_result >> 1 
            if (opposer != 2147483647):  
                line += f"{opposer}" 
            else: 
                line += "TBD"
            if (home == 1): 
                line += " H" 
                home_count += 1
                if (game in saturdays): 
                    saturday_home_count += 1 
            else: 
                line += " A" 
            crossover_cond = False 
            for div in data.divisions: 
                crossover_cond = crossover_cond or (div.isCrossover(team, opposer, data))
            if (crossover_cond): 
                line += " X"

        line = line.ljust(13*(data.num_games + 1) , " ") + f"{home_count}"
        line = line.ljust(len(line) + 5, " ") + f"{saturday_home_count}" 
        print(line) 
def print_json(data): 
    print("here1")  
    if (data.solver.check() != z3.sat): 
        print("Houston... we have a problem") 
        return -1 
    print("here2") 
    model = data.solver.model() 
    solution_games = [[model[data.games[team][game]].as_long() for game in range(data.num_games)] for team in range(data.num_teams)] 
    
    games = {}
    
    for game in range(data.num_games): 
        teams = []  
        for team in range(data.num_teams):
            result = solution_games[team][game]
            result_dict = {} 
            if (result & 1 == 1): 
                result_dict["Home"] = teams_list[team] 
                if (result >> 1 in range(20)): 
                    result_dict["Away"] = teams_list[result >> 1] 
                else: 
                    result_dict["Away"] = "TBD" 
            else:

                if (result >> 1 in range(20)): 
                    result_dict["Home"] = teams_list[result >> 1] 
                else: 
                    result_dict["Home"] = "TBD" 
                result_dict["Away"] = teams_list[team]
            if (team in range(data.red_indices[0], data.red_indices[1] + 1)): 
                result_dict[teams_list[team]] = "Red" 
            elif (team in range(data.blue_indices[0], data.blue_indices[1] + 1)): 
                result_dict[teams_list[team]] = "Blue" 
            else: 
                result_dict[teams_list[team]] = "White" 

            opp = result >> 1 
            
            if (opp in range(data.red_indices[0], data.red_indices[1] + 1)): 
                result_dict[teams_list[opp]] = "Red" 
            elif (opp in range(data.blue_indices[0], data.blue_indices[1] + 1)): 
                result_dict[teams_list[opp]] = "Blue" 
            elif (opp in range(data.white_indices[0], data.white_indices[1] + 1)): 
                result_dict[teams_list[opp]] = "White"
            else: 
                result_dict["TBD"] = "No div"
            teams.append(result_dict) 

        games[str(game)] = teams
    with open("result.json", "w") as f: 
        f.write(str(games))
def main(): 
    # There are 8 meets and 20 teams 
    saturdays = [0, 2, 4,5,7] 
    data = Data(8, 20, wins_and_losses,(0, 6), (7, 12), (13, 19), changed, saturdays) 
    team_gen = TeamGenerator(data)
    print_game_model(data) 
if __name__ == "__main__": 
    main() 
