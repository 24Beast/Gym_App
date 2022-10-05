# Importing Libraries
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QTableWidget, QLabel, QTableWidgetItem, QHeaderView

# Class Definition

class pendingListWidget(QWidget):
    
    def __init__(self,config : dict, db) -> None:
        super().__init__()
        self.db = db
        self.config = config
        self.listWidget = QTableWidget(self)
        self.listWidget.verticalHeader().setVisible(False)
        self.listWidget.horizontalHeader().setVisible(False)
        self.listWidget.setMinimumSize(QtCore.QSize(700,350))
        self.currentRow = 0
        self.headers = ["Member ID","Name","Fee Type","Last Paid"]
        self.numColumns = len(self.headers)
        self.insertHead()
        self.setDisplay()
        self.displayPending()
    
    
    def setDisplay(self) -> None:
        header = self.listWidget.horizontalHeader()
        for i in range(self.numColumns):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)


    def insertHead(self) -> None:
        items = []
        for col,text in enumerate(self.headers):
            self.listWidget.insertColumn(col)
            item = QTableWidgetItem(text)
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            item.setBackground(QColor(self.config["color2"]))
            items.append(item)
        self.insertItems([items])
            
    
    def displayPending(self):
        self.emptyList()
        listItems = self.db.checkDueFees()
        print(f"Number of pending Fees : {len(listItems)}")
        self.insertItems(listItems)
        
        
    def insertItems(self, items : list):
        for item in items:
            self.listWidget.insertRow(self.currentRow)
            for col in range(self.numColumns):
                self.listWidget.setItem(self.currentRow, col, item[col])
            self.currentRow +=1
    
    
    def popItem(self):
        for col in range(self.numColumns):
            self.listWidget.takeItem(self.currentRow,col)
        self.currentRow -= 1
        
        
    def emptyList(self):
        while self.currentRow >= 1:
            self.popItem()
        self.currentRow = 1



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