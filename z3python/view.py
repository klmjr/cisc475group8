import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFormLayout, QLineEdit, QListWidget, QPushButton, QGridLayout, QFileDialog, QComboBox, QMessageBox, QDateTimeEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QDate
from controller import Controller 
class ConstraintLine(QWidget): 
    def __init__(self,parent=None): 
        super(ConstraintLine, self).__init__(parent) 
        self.grid = QGridLayout(self)
        self.dropDown = QComboBox()
        self.list_items = ["Specific opponent", "Specify Home/Away"] 
        self.dropDown.addItems(self.list_items)
        self.dropDown.currentIndexChanged.connect(self.selection_made) 
        self.line_widgets = [] 
        self.grid.addWidget(self.dropDown, 0, 0) 
        self.show_labels_opponents() 
    def clear_line(self): 
        for widget in self.line_widgets: 
            widget.hide()
        self.line_widgets = [] 
    def show_labels_opponents(self): 

        self.clear_line()

        self.team1 = QComboBox()  
        self.team1.addItems(controller.curr_result["teams"]) 
        self.grid.addWidget(self.team1, 0, 1) 

        self.team2 = QComboBox() 
        self.team2.addItems(controller.curr_result["teams"]) 
        self.grid.addWidget(self.team2, 0, 2) 

        self.date = QComboBox() 
        self.date.addItems(controller.dates) 

        self.grid.addWidget(self.date, 0,3) 

        self.line_widgets.append(self.date) 
        self.line_widgets.append(self.team1) 
        self.line_widgets.append(self.team2) 
    def show_labels_home_away(self): 
        self.clear_line()

        self.team = QComboBox() 
        self.team.addItems(controller.curr_result["teams"]) 
        self.home_away = QComboBox() 
        self.home_away.addItems(["Home", "Away"]) 
        self.grid.addWidget(self.team, 0, 1) 
        self.grid.addWidget(self.home_away, 0, 2) 
        
        self.date = QComboBox()
        self.date.addItems(controller.dates) 
        self.grid.addWidget(self.date, 0, 3) 

        
        self.line_widgets.append(self.team) 
        self.line_widgets.append(self.home_away) 
        self.line_widgets.append(self.date) 

    @pyqtSlot() 
    def selection_made(self):

        if (self.dropDown.currentText() == self.list_items[0]): #Specific Opponent
            self.show_labels_opponents()      
        elif (self.dropDown.currentText() == self.list_items[1]): #Home and Away Specification 
            self.show_labels_home_away()
    def finished_adding(self): 
        if (self.dropDown.currentText() == self.list_items[0]): 
            new_constraint = {} 
            new_constraint["team1"] = (self.team1.currentIndex(), self.team1.currentText()) 
            new_constraint["team2"] = (self.team2.currentIndex(), self.team2.currentText()) 
            new_constraint["date"] = self.date.currentText() 
            new_constraint["type"] = "opponent_spec"
            controller.added_constraints.append(new_constraint) 
        elif (self.dropDown.currentText() == self.list_items[1]): 
            new_constraint = {}  
            new_constraint["team"] = (self.team.currentIndex(), self.team.currentText())
            new_constraint["home"] = self.home_away.currentText()
            new_constraint["date"] = self.date.currentText() 
            controller.added_constraints.append(new_constraint) 
class AddConstraints(QWidget): 
    def __init__(self,parent=None): 
        super(AddConstraints, self).__init__(parent) 
        self.input_list = [] 
        self.add_constraint = QPushButton("Add Constraint") 
        self.grid = QGridLayout(self) 
        self.current_row_height = 1
        self.add_constraint.clicked.connect(self.addConstraintLine)
        self.grid.addWidget(self.add_constraint, 0, 0) 
        self.finished_button = QPushButton("Finished")
        self.finished_button.clicked.connect(self.finished_adding) 
        self.grid.addWidget(self.finished_button,1, 0) 
    @pyqtSlot() 
    def addConstraintLine(self):  
        new_constraint = ConstraintLine() 
        self.input_list.append(new_constraint)
        self.grid.removeWidget(self.finished_button) 
        self.grid.addWidget(new_constraint, self.current_row_height, 0) 
        self.current_row_height += 1 
        self.grid.addWidget(self.finished_button, self.current_row_height, 0) 
    @pyqtSlot() 
    def finished_adding(self): 
        global widget
        print("finished adding")
        for lad in self.input_list: 
            lad.finished_adding() 
        widget.getNextWindow()  
class AddTeamLine(QWidget):
    def __init__(self, parent=None): 
        super(AddTeamLine, self).__init__(parent)
        self.team_name = QLineEdit()
        self.team_name.setPlaceholderText("Team Name")
        self.wins = QComboBox() 
        self.wins.addItems(list(map(str, range(20))))  
        self.losses = QComboBox() 
        self.losses.addItems(list(map(str, range(20))))
        self.division = QComboBox()
        self.division.addItems(["Red", "White", "Blue"]) 
        self.grid = QGridLayout()  

        self.grid.addWidget(self.team_name, 0, 0) 
        self.grid.addWidget(self.wins, 0, 1)
        self.grid.addWidget(self.losses, 0, 2)
        self.grid.addWidget(self.division, 0, 3) 
        self.setLayout(self.grid)
    def clicked(self): 
        new_team = {} 
        new_team["team"] = self.team_name.text() 
        new_team["wins"] = int(self.wins.currentText()) 
        new_team["losses"] = int(self.wins.currentText()) 
        new_team["division"] = int(self.wins.currentText())
        controller.add_teams.append(new_team)   
class DeleteTeamLine(QWidget): 
    def __init__(self, parent=None): 
        super(DeleteTeamLine, self).__init__(parent) 
        self.grid = QGridLayout(self) 
        self.dropDown = QComboBox() 
        self.dropDown.addItems(controller.curr_result["teams"])
        
        self.grid.addWidget(self.dropDown, 0, 0) 
    def clicked(self): 
        controller.deleted_teams.append({"team": self.dropDown.currentText(), "number": self.dropDown.currentIndex()}) 
class AddDeleteTeam(QWidget): 
    def __init__(self, parent=None): 
        super(AddDeleteTeam, self).__init__(parent) 
        self.setGeometry(50, 50, 1000, 1000) 
        self.flay = QGridLayout(self)
        self._le = []  
        add_button = QPushButton("+")
        add_button.clicked.connect(self.addTeam) 
        delete_button = QPushButton("-") 
        delete_button.clicked.connect(self.deleteTeam) 
        self.height = 1 
        self.flay.addWidget(QLabel("Add/Delete Teams from list"), 0, 0)
        self.flay.addWidget(add_button, 0, 1) 
        self.flay.addWidget(delete_button, 0, 2) 
        
        self.finished_button = QPushButton("Finished") 
        self.finished_button.clicked.connect(self.finished_adding) 
        self.flay.addWidget(self.finished_button, self.height, 0) 
    @pyqtSlot() 
    def addTeam(self): 
        new_line = AddTeamLine()   
        self._le.append(new_line)
        self.flay.removeWidget(self.finished_button)  
        self.flay.addWidget(QLabel("Add"), self.height, 0) 
        self.flay.addWidget(new_line, self.height, 1) 
        self.height += 1
        self.flay.addWidget(self.finished_button, self.height, 0) 
    @pyqtSlot() 
    def deleteTeam(self): 
        print("delete me")
        new_line = DeleteTeamLine() 
        self._le.append(new_line) 
        self.flay.removeWidget(self.finished_button)  
        self.flay.addWidget(QLabel("Delete"), self.height, 0)
        self.flay.addWidget(new_line, self.height, 1) 
        self.height += 1 
        self.flay.addWidget(self.finished_button, self.height, 0) 
    @pyqtSlot() 
    def finished_adding(self):
        global widget  
        for widge in self._le: 
            widge.clicked()
        widget.getNextWindow()
class SelectFile(QWidget): 
    def __init__(self,name,parent=None): 
        super(SelectFile, self).__init__(parent) 
        self.grid = QFormLayout(self) 
        self.selectFile = QPushButton(name) 
        #self.selectFile.clicked.connect(self.openFile) 
        self.grid.addWidget(self.selectFile)
    def chooseSheet(self, sheets): 
        self.dropDown = QComboBox() 
        self.dropDown.addItems(sheets) 
        self.grid.addRow(self.dropDown)
        self.sheet_choosen = QPushButton("Choose sheet") 
        self.grid.addRow(self.sheet_choosen) 
class AppWindow(QWidget): 
    def __init__(self, parent=None): 
        super(AppWindow, self).__init__(parent) 
        self.grid = QGridLayout() 
        #self.delete_add = AddDeleteTeam()
        self.file_opener = SelectFile("Current Year") 
        self.file_opener.selectFile.clicked.connect(self.read_curr_year) 
        self.prev_file_opener = SelectFile("Previous Year") 
        self.prev_file_opener.selectFile.clicked.connect(self.homeAndAway) 
        self.grid.addWidget(self.file_opener, 0, 0) 
       # self.grid.addWidget(self.delete_add, 1, 0)
        self.finished_button = QPushButton("Finished!") 
        self.finished_button.clicked.connect(self.finished) 
        self.grid.addWidget(self.finished_button, 2, 0) 
        #self.grid.addWidget(AddConstraints(), 3, 0) 
        self.setLayout(self.grid)
    @pyqtSlot() 
    def finished(self):  
        global widget 
        widget.getNextWindow() 
    def openFile(self): 
        dlg = QFileDialog.getOpenFileName(self, "Select Excel file to import","","Excel (*.xls *.xlsx)") 
        filename, file_type = dlg  
        while (filename == ''): 
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Please provide a file")
            msg.setWindowTitle("File Required")
            msg.setDetailedText("A file is required to continue schedule generation")
            msg.setStandardButtons(QMessageBox.Ok)	
            msg.exec_()  
            filename, file_type = QFileDialog.getOpenFileName(self, "Select Excel file to import","","Excel (*.xls *.xlsx)") 
        return filename
    @pyqtSlot()  
    def read_curr_year(self): 
        filename = self.openFile() 
        sheets = controller.getSheetNames(filename, None) 
        self.file_opener.chooseSheet(sheets)
        self.file_opener.sheet_choosen.clicked.connect(lambda: self.readTeams(filename))  
    @pyqtSlot() 
    def readTeams(self, filename):
        curr_sheet = self.file_opener.dropDown.currentText() 

        teams = controller.readTeams(filename, curr_sheet) 
        self.file_opener.hide() 
        self.grid.removeWidget(self.file_opener ) 
        self.grid.addWidget(self.prev_file_opener, 0, 0) 
    @pyqtSlot() 
    def homeAndAway(self): 
        filename = self.openFile() 
        sheets = controller.getSheetNames(filename, None) 
        self.prev_file_opener.chooseSheet(sheets) 
        self.prev_file_opener.sheet_choosen.clicked.connect(lambda: self.homeAndAwayHelper(filename)) 
    @pyqtSlot() 
    def homeAndAwayHelper(self, filename): 
        curr_sheet = self.prev_file_opener.dropDown.currentText() 

        teams = controller.homeAway(filename, curr_sheet)
        self.prev_file_opener.hide()  
        self.grid.removeWidget(self.prev_file_opener)  



class ChooseDates(QWidget): 
    def __init__(self, parent=None): 
        super(ChooseDates, self).__init__(parent) 
        self.year_label = QLabel("Choose year") 
        self.year_choice = QComboBox() 
        self.year_choice.addItems(list(map(str, range(2020, 2100)))) 
        self.year_choice.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.year_choice.setMaxVisibleItems(10)
        self.year_choice.currentIndexChanged.connect(self.selection_made)
        self.grid = QGridLayout(self) 
        self.grid.addWidget(self.year_label, 0, 0) 
        self.grid.addWidget(self.year_choice, 0, 1) 
    @pyqtSlot() 
    def selection_made(self):
        self.games = {} 
        for i in range(8): 
            self.games[f"game{i}"] = QDateTimeEdit()
            self.games[f"game{i}"].setDate(QDate(int(self.year_choice.currentText()), 6, 1)) 
            self.games[f"game{i}"].setCalendarPopup(True)
            self.games[f"game{i}"].setDisplayFormat("MM/dd/yy") 
            self.grid.addWidget(QLabel(f"Game{i + 1}"), i + 1, 0) 
            self.grid.addWidget(self.games[f"game{i}"], i + 1, 1) 
        self.on_finished = QPushButton("Next") 
        self.on_finished.clicked.connect(self.finished_adding) 
        self.grid.addWidget(self.on_finished, 9, 0) 
    @pyqtSlot() 
    def finished_adding(self):
        global widget
        global controller 
        for i in range(8): 
            controller.dates.append(self.games[f"game{i}"].date().toString("MM/dd/yyyy")) 
        widget.getNextWindow() 
        
            
class WindowSwitcher(QWidget): 
    def __init__(self, parent=None): 
        super(WindowSwitcher, self).__init__(parent)
        self.get_initial_window = AppWindow() 
        self.addDeleteTeams = AddDeleteTeam() 
        self.addConstraints = AddConstraints() 
        self.chooseDates = ChooseDates()  
        self.windows = [self.chooseDates, self.get_initial_window, self.addDeleteTeams, self.addConstraints]  
        self.grid = QGridLayout(self) 
        self.currWindow = 0
        self.grid.addWidget(self.windows[self.currWindow], 0, 0) 

    def getNextWindow(self): 
        self.grid.removeWidget(self.windows[self.currWindow]) 
        self.windows[self.currWindow].hide() 
        self.currWindow += 1
        if (self.currWindow > len(self.windows)-1): 
            self.done()
            return 
        self.grid.addWidget(self.windows[self.currWindow], 0, 0)  
    def done(self): 
        print("Done") 
        self.grid.removeWidget(self.windows[self.currWindow-1]) 
        self.grid.addWidget(QLabel("Generating schedule")) 
        print(controller.deleted_teams) 
        print(controller.added_constraints) 
        print(controller.add_teams) 
        #controller.create_schedule() 
    
def window():
   app = QApplication(sys.argv)
   global widget 
   widget = WindowSwitcher()  
   widget.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   controller = Controller()
   window()
