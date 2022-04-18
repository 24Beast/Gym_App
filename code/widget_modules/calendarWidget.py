# Importing Libraries
import sys
sys.path.append("../")
from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QCalendarWidget
from utils.tools import DateTimeToQDate, QDatetoDateTime

MIN_DATE = QDate.fromString("01/01/2022","dd/MM/yyyy")


# Class Definition

class calendarWidget(QWidget):

    def __init__(self, config : dict, db) -> None:
        super().__init__()
        self.db = db
        self.currMemId = -1
        self.config = config
        self.initCalendar()
        self.selectedDates = set()
        self.cellFormat1 = QtGui.QTextCharFormat()
        self.cellFormat1.setBackground(QtGui.QColor("lightblue"))
        self.cellFormat2 = QtGui.QTextCharFormat()
        self.cellFormat2.setBackground(QtGui.QColor("lightgreen"))
    
    
    def initCalendar(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setMinimumDate(MIN_DATE)
        self.calendar.activated.connect(self.select_date)
        self.calendar.setStyleSheet("background-color : lightblue;")

    
    def select_date(self,date) -> None:
        if(date in self.selectedDates):
            self.selectedDates.discard(date)
            self.calendar.setDateTextFormat(date, self.cellFormat1)
            if(self.currMemId!=-1):
                self.db.removeCalender(QDatetoDateTime(date), self.currentMemId)
        else:
            self.selectedDates.add(date)
            self.calendar.setDateTextFormat(date, self.cellFormat2)
            if(self.currMemId!=-1):
                self.db.addCalender(QDatetoDateTime(date), self.currentMemId)
            
            
    def refresh_calendar(self) -> None:
        self.currMemId = -1
        self.selectedDates = set()
        iterDate = MIN_DATE
        currDate = QDate.currentDate()
        while iterDate<currDate:
            self.calendar.setDateTextFormat(iterDate, self.cellFormat1)
    
    
    def getMemeberCalendar(self,MemId : int) -> None:
        self.refresh_calendar()
        self.currMemId = MemId
        dates  = db.fetchCalender(MemId)
        for date in dates:
            self.select_date(DateTimeToQDate(date))
        
            

if __name__ == "__main__":    
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from utils.DBManager import DBManager
    from utils.tools import getConfig
    
    config = getConfig()
    db = DBManager(config)
    
    App = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setGeometry(0, 0, 400, 300)
    
    calendar = calendarWidget(config,db)
    window.setCentralWidget(calendar)
    window.show()
    
    sys.exit(App.exec_())