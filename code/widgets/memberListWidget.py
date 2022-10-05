# Importing Libraries
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QListWidget

# Class Definition

class memberListWidget(QWidget):
    
    def __init__(self,config : dict, db) -> None:
        super().__init__()
        self.db = db
        self.config = config
        self.listWidget = QListWidget(self)
        self.listWidget.setMinimumSize(QtCore.QSize(700,350))
        self.currentRow = 0
        self.currentPage = 1
        self.displayPage(self.currentPage)
    
    
    def displayPage(self, page = -1):
        self.emptyList()
        if(page!=-1):
            self.currentPage = page
        listItems = self.db.getMemberPage(self.currentPage)
        self.insertItems(listItems)
        
        
    def insertItems(self, items : list):
        for item in items:
            self.listWidget.insertItem(self.currentRow, item)
            self.currentRow +=1
    
    
    def popItem(self):
        self.listWidget.takeItem(self.currentRow)
        self.currentRow -= 1
        
        
    def emptyList(self):
        while self.currentRow >= 0:
            self.popItem()
        self.currentRow = 0



if __name__ == "__main__":    
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from utils.DBManager import DBManager
    from utils.tools import getConfig
    
    config = getConfig()

    db = DBManager(config)

    App = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(0, 0, 800, 600)

    lwidget = memberListWidget(config,db)
    window.setCentralWidget(lwidget)
    window.show()

    sys.exit(App.exec_())