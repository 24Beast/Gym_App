# Importing Libraries
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem

# Class Definition

class memberListWidget(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        self.listWidget = QListWidget(self)
        self.currentRow = 0
        
    
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
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = QMainWindow()
    window.setGeometry(0, 0, 400, 300)
    #Add List
    lwidget = memberListWidget()
    window.setCentralWidget(lwidget)
    window.show()
    # start the app
    sys.exit(App.exec_())