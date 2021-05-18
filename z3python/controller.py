
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
        return self.prev_result
    def create_schedule(self): 

        make_me_schedule(self.curr_result["wl_ratios"],self.curr_result["teams"],self.changed,self.prev_result["home_and_away"], self.curr_result["indices"]["red"], self.curr_result["indices"]["white"], self.curr_result["indices"]["blue"])    
        
    def updateTeams(self): 
        # update Changed 
        # update wl_ratios 
        # update teams 
        # update home_away
        # update indices 
        pass 
