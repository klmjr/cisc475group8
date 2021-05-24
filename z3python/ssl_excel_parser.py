import numpy as np
import pandas as pd
from copy import deepcopy 
import xlrd 
import xlwt 
import calendar 
# Read Previous Years Division Bye Numbers and Update the file to Hold this years Bye and return a Dictionary of the number of Byes 
# For each Division 
def getCurrentYearByes(filename, year): 
    pass
# Read which teams have not had a bye in the past few years 
# Return them to be targeted by the solver 
def getPossibleTeams(filename, year, team_names, sheet): 
    # first get the correct year
    
    wb = xlrd.open_workbook(filename)
    sheet = wb.sheet_by_name(sheet) 
    
    year_start = 4 
    year_start_col = 2 

    

    # then find the teams that haven't had a bye in the past few years and append them to an array 

    
def write_excel(year, directory, dates, model, teams, indices, win_loss): 
    wb = xlwt.Workbook() 
    sheet = wb.add_sheet("New schedule") 

    curr_index = 0 
    start_index = 7 
    #print(dates)
    
    weekdays = [] 

    for c in dates: 
        month, day, year = c.split("/")
        month = int(month) 
        day = int(day) 
        year = int(year) 
        weekdays.append(calendar.day_name[calendar.weekday(year, month, day)] )

    sheet.write(6, 1, "RED")
    curr_index = 7 
    date_index = 0 
    for col in range(ord("E")-ord("A"), ord("S")-ord("A")+1, 2): 
        sheet.write(4, col, weekdays[date_index])
        sheet.write(5, col, dates[date_index]) 
        date_index += 1 
    for i in range(indices["red"][0], indices["red"][1] + 1): 
        sheet.write(curr_index, 1, teams[i])
        sheet.write(curr_index, 0, str(i))
        w, l = win_loss[i]["ratio"] 
        win_loss_string = f"{w}-{l}"
        sheet.write(curr_index, 2, win_loss_string)
        model_col = 0 
        home_count = 0
        for col in range(ord("E")-ord("A"), ord("S")-ord("A")+1, 2): 
            if (model[i][model_col] & 1 == 1): 
                write_here = f"{i}-{model[i][model_col] >> 1}"
                home_count += 1 
            else: 
                write_here = f"{model[i][model_col] >> 1}-{i}" 
            if (model[i][model_col] >> 1 not in range(indices["red"][0], indices["red"][1] + 1)):
                style = xlwt.easyxf("font:color-index red") 
            else: 
                style = xlwt.easyxf("font:color-index black") 
            sheet.write(curr_index, col, write_here, style) 
            model_col += 1
        sheet.write(curr_index, ord("S") - ord("A") + 2, str(home_count)) 
        curr_index += 1 
    
    curr_index +=2 
    sheet.write(curr_index, 1, "WHITE") 

    curr_index += 1 
    for i in range(indices["white"][0], indices["white"][1] + 1): 
        sheet.write(curr_index, 1, teams[i])
        sheet.write(curr_index, 0, str(i))
        model_col = 0 
        home_count = 0
        w, l = win_loss[i]["ratio"] 
        win_loss_string = f"{w}-{l}"
        sheet.write(curr_index, 2, win_loss_string)
        for col in range(ord("E")-ord("A"), ord("S")-ord("A")+1, 2): 
            if (model[i][model_col] & 1 == 1): 
                write_here = f"{i}-{model[i][model_col] >> 1}"
                home_count += 1 
            else: 
                write_here = f"{model[i][model_col] >> 1}-{i}" 
            if (model[i][model_col] >> 1 not in range(indices["white"][0], indices["white"][1] + 1)):
                style = xlwt.easyxf("font:color-index red") 
            else: 
                style = xlwt.easyxf("font:color-index black") 
            sheet.write(curr_index, col, write_here, style) 
            model_col += 1
        sheet.write(curr_index, ord("S") -ord("A") + 2, str(home_count))
        curr_index += 1 

    
    curr_index +=2 
    sheet.write(curr_index, 1, "BLUE") 
    curr_index += 1 
    for i in range(indices["blue"][0], indices["blue"][1] + 1): 
        sheet.write(curr_index, 1, teams[i])
        sheet.write(curr_index, 0, str(i))
        model_col = 0 
        home_count = 0 
        w, l = win_loss[i]["ratio"] 
        win_loss_string = f"{w}-{l}"
        sheet.write(curr_index, 2, win_loss_string)
        for col in range(ord("E")-ord("A"), ord("S")-ord("A")+1, 2): 
            if (model[i][model_col] & 1 == 1): 
                write_here = f"{i}-{model[i][model_col] >> 1}"
                home_count +=1  
            else: 
                write_here = f"{model[i][model_col] >> 1}-{i}" 
            if (model[i][model_col] >> 1 not in range(indices["blue"][0], indices["blue"][1] + 1)):
                style = xlwt.easyxf("font:color-index red") 
            else: 
                style = xlwt.easyxf("font:color-index black") 
            sheet.write(curr_index, col, write_here, style) 
            model_col += 1 
        sheet.write(curr_index, ord("S") - ord("A") + 2, str(home_count)) 
        curr_index += 1 
    wb.save("test.xls") 
# After the solver has determined which teams have had a bye, update the spreadsheet to indicate those teams had a bye this year
def updateTeamByes(filename, year): 
    pass 
# calculated home or away based on the "n - n" format where n is any team number. it follows HOME - AWAY. 1 is home, 0 is away
def home_or_away(team_number, weeks):
  home_or_away_array = []
  for week in weeks:
    week_temp = week.split(" - ")
    if int(team_number) == int(week_temp[0]):
      home_or_away_array.append(1)
    else:
      home_or_away_array.append(0)
  return home_or_away_array

# Returns the array of teams and indices of red, white, and blue divisions in the array 
def getTeams(filename, sheetname): 
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_name(sheetname)  
    curr_index = 0 
    curr_division = None 
    teams = [] 
    red_start = 0 
    red_end = 0 
    white_start = 0 
    white_end = 0 
    blue_start = 0 
    blue_end = 0
    wl_ratios = [] 
    changed = [] 
    for row_idx in range(sheet.nrows): 
        curr_contents = sheet.cell(row_idx, 1).value 
        if (curr_contents == "RED"): 
            curr_division = "RED"
            red_start = curr_index  
            continue 
        elif (curr_contents == "BLUE"): 
            curr_division = "BLUE" 
            blue_start = curr_index 
            continue 
        elif (curr_contents == "WHITE"): 
            curr_division = "WHITE"
            white_start = curr_index 
            continue 
        if not(curr_division):
            continue 
        if (len(curr_contents) == 0 and curr_division == "BLUE"): 
            blue_end = curr_index - 1 
            curr_division = None 
            break 
        if ("---" in curr_contents): 
            continue 
        if (len(curr_contents) == 0 and curr_division == "RED"): 
            red_end = curr_index - 1 
            curr_division = None 
            continue 
        if (len(curr_contents) == 0 and curr_division == "WHITE"): 
            white_end = curr_index - 1 
            curr_division = None 
            continue 
        if ("*" in curr_contents): 
            changed.append(curr_index) 
        teams.append(curr_contents) 
        w, l = sheet.cell(row_idx, 2).value.split("-") 
        wl_ratios.append({"team": curr_index, "ratio": (int(w), int(l))}) 

        curr_index += 1
    
    red_indices = (red_start, red_end) 
    blue_indices = (blue_start, blue_end) 
    white_indices = (white_start, white_end) 

    indices = {"red": red_indices, "white": white_indices, "blue": blue_indices}  


    return {"teams": teams, "indices": indices, "wl_ratios": wl_ratios, "changed": changed}
def getHomeAway(previous_year_file, sheetname): 
    row_start = 7 
    workbook = xlrd.open_workbook(previous_year_file) 
    sheet = workbook.sheet_by_name(sheetname) 
    num_teams = 0 
    rows_w_teams = []
    red_indices = [0]*2 
    white_indices = [0]*2 
    blue_indices = [0]*2 
    curr_index = 0
    curr_division = None
    teams = [] 
    for row_idx in range(row_start-1, sheet.nrows): 
        curr_contents = sheet.cell(row_idx, 1).value 
        if (curr_contents == "RED"): 
            curr_division = "RED"
            red_indices[0] = curr_index  
            continue 
        elif (curr_contents == "BLUE"): 
            curr_division = "BLUE" 
            blue_indices[0] = curr_index 
            continue 
        elif (curr_contents == "WHITE"): 
            curr_division = "WHITE"
            white_indices[0]  = curr_index 
            continue 
        if not(curr_division):
            continue 
        if (len(curr_contents) == 0 and curr_division == "BLUE"): 
            blue_indices[1] = curr_index - 1 
            curr_division = None 
            break 
        if ("---" in curr_contents): 
            continue 
        if (len(curr_contents) == 0 and curr_division == "RED"): 
            red_indices[1] = curr_index - 1 
            curr_division = None 
            continue 
        if (len(curr_contents) == 0 and curr_division == "WHITE"): 
            white_indices[1] = curr_index - 1 
            curr_division = None 
            continue 
        rows_w_teams.append(row_idx) 
        teams.append(curr_contents) 
        curr_index += 1
    
    home_and_away = [[0 for i in range(8)] for j in range(curr_index)]  
    
    games_col_start = 4
    curr_index = 0
     
    for col in range(ord("E")-ord("A"), ord("S")-ord("A")+1, 2): 
        for i in range(len(rows_w_teams)): 
            curr_row = rows_w_teams[i] 
            val = sheet.cell(curr_row, col).value
            if ("BYE" in val):
                home_and_away[i][curr_index] = -1 
                continue 
            first = int(val.replace(" ", "").split('-')[0])
            curr_team = int(sheet.cell(curr_row, 0).value) 
            if (first == curr_team):
                home_and_away[i][curr_index] = 1
        curr_index += 1
    home_away_map = {} 
    for i in range(len(home_and_away)): 
        home_away_map[teams[i].replace("*", "")] = home_and_away[i]
    return {"teams": teams, "indices": {"red": red_indices, "white":white_indices, "blue": blue_indices}, "home_and_away": home_away_map}
def parse_excel(filename): 
  # append first three cols that have team name, number, and win ratio
  cols = ["A", "B", "C"]
  # append alternating columns assuming columns in between are blank (as all schedules have been)
  for i in range(ord("E"), ord("V"), 2):
    cols.append(str(chr(i)))
  cols.append("V")
  # puts columns into a string to then parse
  columns_to_parse = ""
  for i in range(len(cols)):
    if i < len(cols)-1:
      columns_to_parse += str(cols[i]) + ", "
    else:
      columns_to_parse += str(cols[i])
  # reads excel file with columns specified, skips beginning rows, arbitrary format: need to change name for different excel files and sheet names
  df = pd.read_excel(filename, sheet_name="Odd year template", usecols=columns_to_parse, skiprows=[i for i in range(5)])
  # format of data frame that was parsed
  df.columns = ['Team Number', 'Team Name', 'Win/Loss Ratio', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Home Total', 'Meets Sat']
  #arbitrary code that is theoretically redundant but vital to the program :)
  df_team_divisions = df.copy()
  df_team_divisions.rename(columns={"Unnamed: 0": "Team Number", "Unnamed: 1": "Team Name", "Unnamed: 2": "Win/Loss Ratio"},inplace=True)

  # clears "NaN" rows where data is pointless to clean up the dataframe to only necessary information
  for i in df:
    df = df[df[i].notna()]
  df_team_divisions = df_team_divisions[df_team_divisions["Team Name"].notna()]
  df["Team Number"] = df["Team Number"].astype(int)
  pd.set_option("display.max_rows", None, "display.max_columns", None)

  # n is the final column where "HOME - AWAY" is located, we use this index to determine how many players are on the team.
  # the following code parses from RED to WHITE, WHITE to BLUE, and BLUE to "HOME - AWAY" in order to get a variable amount of teams based on spreadsheet.
  n = 0
  red = 0
  blue = 0
  white = 0
  team_names = df_team_divisions["Team Name"].to_numpy()

  for i in range(len(team_names)):
    if team_names[i] == "RED":

      red = i
    if team_names[i] == "BLUE":
      blue = i
    if team_names[i] == "WHITE":
      white = i
    if team_names[i] == "HOME - AWAY":
      n = i
  df_team_divisions.drop(df_team_divisions.tail(len(df_team_divisions)-n).index, inplace=True)


  red_team = np.asarray([team_names[index] for index in range(red+1, white, 1)])
  white_team = np.asarray([team_names[index] for index in range(white+1, blue, 1)])
  blue_team = np.asarray([team_names[index] for index in range(blue+1, n, 1)])
  red_indices = (0, len(red_team) - 1) 
  white_indices = (len(red_team), len(red_team) + len(white_team) - 1) 
  blue_indices = (len(red_team) + len(white_team), len(red_team) + len(white_team) + len(blue_team) - 2) 
  print(red_team, white_team, blue_team) 
  print(red_indices, white_indices, blue_indices) 
  #arbitrary dataframes created for the sake of readability for respective teams
  red_df = pd.DataFrame(red_team, columns=["RED"])
  white_df = pd.DataFrame(white_team, columns=["WHITE"])
  blue_df = pd.DataFrame(blue_team, columns=["BLUE"])
  team_dfs = [red_df, white_df, blue_df]
  df_team_divisions = pd.DataFrame()
  df_team_divisions = pd.concat(team_dfs, axis=1)

  #appends red teams to red_team_full_df which contains everything from win/loss record to home/away weeks
  red_team_full_df = pd.DataFrame()
  white_team_full_df = pd.DataFrame()
  blue_team_full_df = pd.DataFrame()
  for i in red_team:
    red_team_full_df = red_team_full_df.append(df[df["Team Name"] == i], ignore_index=True)
  for i in white_team:
    white_team_full_df = white_team_full_df.append(df[df["Team Name"] == i], ignore_index=True)
  for i in blue_team:
    blue_team_full_df = blue_team_full_df.append(df[df["Team Name"] == i], ignore_index=True)
  win_loss_array = df["Win/Loss Ratio"].to_numpy()
  # formats win/loss to be in tuple format per our program
  win_loss_array = [eval(i.replace("-", ",")) for i in win_loss_array]
  team_numbers = df["Team Number"].to_numpy()

  team_wl_dict = [{"team":team_numbers[i], "ratio":win_loss_array[i]} for i in range(len(win_loss_array))]

  #iterates through each team in each respective division to allow creating the "home/away" matrix (this is very redundant but it works)
  red_team_home_or_away = []
  white_team_home_or_away = []
  blue_team_home_or_away = []
  for row in red_team_full_df.iterrows():
    team_number = row[1][0]
    # row[1][0] is team number and the rest follows the following format
    # ['Team Number', 'Team Name', 'Win/Loss Ratio', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Home Total', 'Meets Sat']
    # although we only grab up to week 8
    weeks = [row[1][3],row[1][4],row[1][5],row[1][6],row[1][7],row[1][8],row[1][9],row[1][10]]
    #home_or_away just returns an array to be appended such that it shows 1 for home or 0 for away for each respective week for the 8 weeks
    red_team_home_or_away.append(home_or_away(team_number, weeks))

  for row in white_team_full_df.iterrows():
    team_number = row[1][0]
    weeks = [row[1][3],row[1][4],row[1][5],row[1][6],row[1][7],row[1][8],row[1][9],row[1][10]]
    white_team_home_or_away.append(home_or_away(team_number, weeks))

  for row in blue_team_full_df.iterrows():
    team_number = row[1][0]
    weeks = [row[1][3],row[1][4],row[1][5],row[1][6],row[1][7],row[1][8],row[1][9],row[1][10]]
    blue_team_home_or_away.append(home_or_away(team_number, weeks))
  #appends all respective teams to a specific home_away array
  home_away = []
  for i in red_team_home_or_away:
    home_away.append(i)
  for i in white_team_home_or_away:
    home_away.append(i)
  for i in blue_team_home_or_away:
    home_away.append(i)
  #print(home_away)

  # shows all teams that contain an *
  red_teams_moved = red_team_full_df[red_team_full_df["Team Name"].str.contains("\*")]
  white_teams_moved = white_team_full_df[white_team_full_df["Team Name"].str.contains("\*")]
  blue_teams_moved = blue_team_full_df[blue_team_full_df["Team Name"].str.contains("\*")]

  white_to_red = 0
  blue_to_white = 0
  white_to_blue = 0
  red_to_white = 0

  for row in red_teams_moved.iterrows():
    team_number = row[1][0]
    win_loss = row[1][2].split("-")
    if (int(win_loss[0]) != 0):
      if(int(win_loss[0])+int(win_loss[1]))/int(win_loss[0]) > .5:
        white_to_red = team_number

  for row in white_teams_moved.iterrows():
    team_number = row[1][0]
    win_loss = row[1][2].split("-")
    if (int(win_loss[0]) != 0):
      if(int(win_loss[0])+int(win_loss[1]))/int(win_loss[0]) > .5:
        blue_to_white = team_number
      else:
        red_to_white = team_number
    else:
      red_to_white = team_number

  for row in blue_teams_moved.iterrows():
    team_number = row[1][0]
    win_loss = row[1][2].split("-")
    if(int(win_loss[0]) != 0):
      if(int(win_loss[0])+int(win_loss[1]))/int(win_loss[0]) < .5:
        white_to_blue = team_number
    else:
      white_to_blue = team_number
  changed = {}

  if white_to_red != 0:
    changed["white_to_red"] = white_to_red
  if blue_to_white != 0:
    changed["blue_to_white"] = blue_to_white
  if white_to_blue != 0:
    changed["white_to_blue"] = white_to_blue
  if red_to_white != 0:
    changed["red_to_white"] = red_to_white

  #print(changed)

  #the data you need from this file are the following (this is just me changing variable names to match the conventions from swim_data.py)

  #added this block of code so that I remove the * from all team names in the list
  teams = df["Team Name"].to_numpy()
  for i in range(len(teams)):
    if teams[i][len(teams[i])-1] == "*":
      teams[i] = teams[i][:-1]

  wins_losses = win_loss_array
  wins_and_losses = [deepcopy(c) for c in team_wl_dict] 

  #wins and losses in tuple form of (w, l)
  #print(wins_losses)

  #wins and losses in tuple form with corresponding team ('team':number, 'ratio': (w,l))
  #print(wins_and_losses)

  #all team names
  #print(teams)

  #all changed teams (for now it only works for one team per division as to not break code per landons advice
  #print(changed)

  #all home / away teams in a single array
  #print(home_away)
  for i in range(len(teams)): 
      wins_and_losses[i]['team'] = i
  print(wins_and_losses)
  print(team_wl_dict) 
  for key in changed: 
      for i in range(len(team_wl_dict)):
          found = False 
          if (changed[key] == team_wl_dict[i]['team']): 
              changed[key] = wins_and_losses[i]['team'] 
              found = True
              print("Hm") 
          if (found): 
              break
  return wins_and_losses, teams, changed, home_away, red_indices, white_indices, blue_indices

def getChanged(changed_teams, curr_teams, prev_teams, curr_indices, prev_indices): 
    changed = {}

    for team in changed_teams: 
        for other in range(len(prev_teams)): 
            if (prev_teams[other].replace("*", "") == curr_teams[team].replace("*", "")):
                white_to_red = team in range(curr_indices["red"][0], curr_indices["red"][1] + 1)
                white_to_red = white_to_red and other in range(prev_indices["white"][0], prev_indices["white"][1] + 1) 

                red_to_white = team in range(curr_indices["white"][0], curr_indices["white"][1] + 1) 
                red_to_white = red_to_white and other in range(prev_indices["red"][0], prev_indices["red"][1] + 1) 

                white_to_blue = team in range(curr_indices["blue"][0], curr_indices["blue"][1] + 1) 
                white_to_blue = white_to_blue and other in range(prev_indices["white"][0], prev_indices["white"][1] + 1) 

                blue_to_white = team in range(curr_indices["white"][0], curr_indices["white"][1] + 1) 
                blue_to_white = blue_to_white and other in range(prev_indices["blue"][0], prev_indices["blue"][1] + 1) 

                if (white_to_red): 
                    changed["white_to_red"] = team
                elif (red_to_white): 
                    changed["red_to_white"] = team
                elif (white_to_blue): 
                    changed["white_to_blue"] = team 
                elif (blue_to_white): 
                    changed["blue_to_white"] = team 
    return changed 



# Update teams and the divisions indices... determine if bye meets are necessary 
def updateTeams(teams_to_add, teams_to_delete, data): 
    win_loss = updateWinLoss(data.current_filename, data.teams) 
    pass 
#if __name__ == "__main__": 
def parse_excel_two(): 
    curr_result = getTeams("2019_schedule.xls", "Odd year template") 
    prev_result = getHomeAway("2018_schedule.xls", "Odd year template") 
    
    changed = getChanged(curr_result["changed"], curr_result["teams"], prev_result["teams"], curr_result["indices"], prev_result["indices"])  

    return curr_result["wl_ratios"],curr_result["teams"],changed,prev_result["home_and_away"], curr_result["indices"]["red"], curr_result["indices"]["white"], curr_result["indices"]["blue"]    

if __name__ == "__main__": 
    #getPossibleTeams("crossover_meets_new.xls", 2020, [], "Byes")  

    write_excel(None, None, None, None, None, None) 
