
from ssl_excel_parser import getTeams, getHomeAway, getChanged 
from team_generator import make_me_schedule  
import xlrd 
class Controller(): 
    def __init__(self):
        self.deleted_teams = [] 
        self.added_constraints = [] 
        self.dates = []
        self.add_teams = [] 
        pass 
    def getSheetNames(self, filename, spreadsheet): 
        wb = xlrd.open_workbook(filename) 
        return wb.sheet_names()
    def readTeams(self, filename, spreadsheet): 
        self.curr_result = getTeams(filename, spreadsheet)  
        return self.curr_result
    def homeAway(self, filename, spreadsheet): 
        self.prev_result = getHomeAway(filename, spreadsheet) 
        self.changed = getChanged(self.curr_result["changed"], self.curr_result["teams"], self.prev_result["teams"], self.curr_result["indices"], self.prev_result["indices"])

        home_away = [[] for i in range(len(self.curr_result["teams"]))] 

        for i in range(len(self.curr_result["teams"])): 
            if (self.curr_result["teams"][i].replace("*", "") in self.prev_result["home_and_away"]): 
                home_away[i] = self.prev_result["home_and_away"][self.curr_result["teams"][i].replace("*", "")] 
            else: 
                home_away[i] = [-1 for i in range(8)]
                print(self.curr_result["teams"][i])
        self.curr_result["home_and_away"] = home_away
        return self.prev_result
    def create_schedule(self): 
        if (len(self.curr_result["teams"]) % 2 == 1 ): 
            self.byes = True 
        else: 
            self.byes = False 
        make_me_schedule(self.curr_result["wl_ratios"],self.curr_result["teams"],self.changed,self.curr_result["home_and_away"], self.curr_result["indices"]["red"], self.curr_result["indices"]["white"], self.curr_result["indices"]["blue"], self.byes, self.dates)    
    def updateTeamsHelperAdd(self, team, division, wl):
        if (division == "RED"): 
            self.curr_result["teams"] = self.curr_result["teams"][:self.curr_result["indices"]["red"][1] + 1] + [team] + self.curr_result["teams"][self.curr_result["indices"]["white"][0]:]

            self.curr_result["wl_ratios"] = self.curr_result["wl_ratios"][:self.curr_result["indices"]["red"][1] + 1] + [{"team":self.curr_result["indices"]["red"][1] + 1, "ratio": wl}] + self.curr_result["wl_ratios"][self.curr_result["indices"]["white"][0]:]

            replace = [-1 for i in range(8)] 
            self.curr_result["home_and_away"] = self.curr_result["home_and_away"][:self.curr_result["indices"]["red"][1] + 1] + [replace] + self.curr_result["home_and_away"][self.curr_result["indices"]["white"][0]:] 

            new_blue_start = self.curr_result["indices"]["blue"][0] + 1 
            new_blue_end = self.curr_result["indices"]["blue"][1] + 1 
            new_red_start = self.curr_result["indices"]["red"][0] 
            new_red_end = self.curr_result["indices"]["red"][1] + 1
            new_white_start = self.curr_result["indices"]["white"][0] + 1
            new_white_end = self.curr_result["indices"]["white"][1] + 1
            self.curr_result["indices"]["blue"] = (new_blue_start, new_blue_end) 
            self.curr_result["indices"]["white"] = (new_white_start, new_white_end) 
            self.curr_result["indices"]["red"] = (new_red_start, new_red_end)

            # update w/l ratio indices 
            for i in range(self.curr_result["indices"]["white"][0], len(self.curr_result["wl_ratios"])): 
                self.curr_result["wl_ratios"][i]["team"] += 1 
            
            for key in self.changed: 
                if (key.split("_")[-1] != "red"): 
                    self.changed[key] += 1 
            pass 
        elif (division == "BLUE"):
            self.curr_result["teams"] = self.curr_result["teams"] + [team] 
            self.curr_result["wl_ratios"] = self.curr_result["wl_ratios"] + [{"team":len(self.curr_result["teams"]) - 1, "ratio": wl}]
            replace = [-1 for i in range(8)]
            self.curr_result["home_and_away"] = self.curr_result["home_and_away"] + [replace] 
            new_blue_end = self.curr_result["indices"]["blue"][1] + 1 
            new_blue_start = self.curr_result["indices"]["blue"][0] 
            self.curr_result["indices"]["blue"] = (new_blue_start, new_blue_end) 
            pass 
        elif (division == "WHITE"):
            new_row = [-1 for i in range(8)] 
            self.curr_result["teams"] = self.curr_result["teams"][:self.curr_result["indices"]["white"][1] + 1] + [team] + self.curr_result["teams"][self.curr_result["indices"]["blue"][0]:]
            self.curr_result["wl_ratios"] = self.curr_result["wl_ratios"][:self.curr_result["indices"]["white"][1] + 1] + [{"team": self.curr_result["indices"]["white"][1] + 1, "ratio": wl} ] + self.curr_result["wl_ratios"][self.curr_result["indices"]["blue"][0]:]  
            self.curr_result["home_and_away"] = self.curr_result["home_and_away"][:self.curr_result["indices"]["white"][1] + 1] + [new_row] + self.curr_result["home_and_away"][self.curr_result["indices"]["blue"][0]:]
            
            new_white_end = self.curr_result["indices"]["white"][1] + 1 
            new_white_start = self.curr_result["indices"]["white"][0] 

            new_blue_start = self.curr_result["indices"]["blue"][0] + 1 
            new_blue_end = self.curr_result["indices"]["blue"][1] + 1 
            self.curr_result["indices"]["blue"] = (new_blue_start, new_blue_end) 
            self.curr_result["indices"]["white"] = (new_white_start, new_white_end) 

            # update w/l ratio indices 
            for i in range(self.curr_result["indices"]["blue"][0], len(self.curr_result["wl_ratios"])): 
                self.curr_result["wl_ratios"][i]["team"] += 1 
            
            for key in self.changed: 
                if (key.split("_")[-1] == "blue"): 
                    self.changed[key] += 1 

        

    def updateTeams(self): 
        # update Changed 
        # update wl_ratios 
        # update teams 
        # update home_away
        # update indices 
        for team in self.add_teams: 
            self.updateTeamsHelperAdd(team["team"], team["division"], (team["wins"], team["losses"]))  
        pass 
