# Importing Libraries
from PyQt5 import QtCore
from calendarWidget import calendarWidget
from pendingListWidget import pendingListWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout

# Class Definition

class rightWidget(QWidget):
    
    def __init__(self,config : dict, db) -> None:
        super().__init__()
        self.db = db
        self.config = config
        self.initLayout()
    
    def initLayout(self):
        self.layout = QVBoxLayout()
        # Add widgets to the layout
        self.layout.addWidget(calendarWidget(self.config, self.db))
        self.layout.addWidget(pendingListWidget(self.config, self.db))
        self.setLayout(self.layout)



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

    rwidget = rightWidget(config,db)
    window.setCentralWidget(rwidget)
    window.show()

    sys.exit(App.exec_())