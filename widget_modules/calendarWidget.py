# Importing Libraries
from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget,QCalendarWidget


MIN_DATE = QDate.fromString("01/01/2022","dd/MM/yyyy")


# Class Definition

class calendarWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
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
        else:
            self.selectedDates.add(date)
            self.calendar.setDateTextFormat(date, self.cellFormat2)
            
            
    def refresh_calendar(self) -> None:
        self.selectedDates = set()
        iterDate = MIN_DATE
        currDate = QDate.currentDate()
        while iterDate<currDate:
            self.calendar.setDateTextFormat(iterDate, self.cellFormat1)
            

if __name__ == "__main__":    
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = QMainWindow()
    window.setGeometry(0, 0, 400, 300)
    #Add Calendar
    calendar = calendarWidget()
    window.setCentralWidget(calendar)
    window.show()
    # start the app
    sys.exit(App.exec_())