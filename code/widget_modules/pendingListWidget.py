# Importing Libraries
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QListWidget, QLabel, QListWidgetItem

# Class Definition

class pendingListWidget(QWidget):
    
    def __init__(self,config : dict, db) -> None:
        super().__init__()
        self.db = db
        self.config = config
        self.listWidget = QListWidget(self)
        self.listWidget.setMinimumSize(QtCore.QSize(450,300))
        self.currentRow = 0
        self.displayPending()
    
    
    def insertHead(self) -> None:
        item = QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        text = "Member ID \t     Name   \t\t  Fee Type \t    Last Paid"
        item.setBackground(QColor(self.config["color2"]))
        item.setText(text)
        self.insertItems([item])
            
    
    def displayPending(self):
        self.emptyList()
        self.insertHead()
        listItems = self.db.checkDueFees()
        print(len(listItems))
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
    sys.path.append("../")
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from utils.DBManager import DBManager
    from utils.tools import getConfig
    
    config = getConfig()

    db = DBManager(config)

    App = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(0, 0, 800, 600)

    pwidget = pendingListWidget(config,db)
    window.setCentralWidget(pwidget)
    window.show()

    sys.exit(App.exec_())