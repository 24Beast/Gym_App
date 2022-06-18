# Importing Libraries
import datetime
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QFormLayout, QHBoxLayout, QPushButton

# Class Definition

class memberFormWidget(QWidget):
    
    def __init__(self,config : dict, db) -> None:
        super().__init__()
        self.db = db
        self.config = config
        self.feeKey = {1 : "Monthly", 3 : "Quaterly", 6 : "Half Yearly", 12 : "Yearly"}
        self.feeKeyRev = {"Monthly" : 1, "Quaterly" : 3 , "Half Yearly" : 6, "Yearly" : 12}
        self.submitButton = QPushButton(text = "Submit")
        self.submitButton.clicked.connect(self.setFormInfo)
        self.backButton = QPushButton("Back")
        self.initLayout()
        
    def initLayout(self):
        self.layout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.leftLayout.addRow(QLabel("Name :"), QLineEdit())
        self.leftLayout.addRow(QLabel("DOB :"), QLineEdit())
        self.leftLayout.addRow(QLabel("Residential Address:"), QLineEdit())
        self.leftLayout.addRow(QLabel("Business Address :"), QLineEdit())
        self.leftLayout.addRow(QLabel("Fee :"), QLineEdit())
        self.leftLayout.addRow(QLabel("LastPaid: "), QLineEdit())
        self.rightLayout = QFormLayout()
        self.rightLayout.addRow(QLabel("MemID :"), QLineEdit())
        self.rightLayout.addRow(QLabel("Father's Name :"), QLineEdit())
        self.rightLayout.addRow(QLabel("Residential Number :"), QLineEdit())
        self.rightLayout.addRow(QLabel("Business Number :"), QLineEdit())
        self.rightLayout.addRow(QLabel("Fee Type :"), QLineEdit())
        self.rightLayout.addRow(self.submitButton)
        self.layout.addLayout(self.leftLayout)
        self.layout.addLayout(self.rightLayout)
        self.layout.addWidget(self.backButton)
        self.setLayout(self.layout)
        
    
    def getFormInfo(self, MemId : str):
        if(MemId == "NA"):
            self.leftLayout.itemAt(1).widget().setText(" ")
            self.leftLayout.itemAt(3).widget().setText("2000-01-01 00:00:00")
            self.leftLayout.itemAt(5).widget().setText(" ")
            self.leftLayout.itemAt(7).widget().setText(" ")
            self.leftLayout.itemAt(9).widget().setText(" ")
            self.leftLayout.itemAt(11).widget().setText("2022-01-01 00:00:00")
            self.rightLayout.itemAt(1).widget().setText(MemId)
            self.rightLayout.itemAt(3).widget().setText(" ")
            self.rightLayout.itemAt(5).widget().setText(" ")
            self.rightLayout.itemAt(7).widget().setText(" ")
            self.rightLayout.itemAt(9).widget().setText("Monthly")
            return
        data = self.db.getMemberInfo(MemId)
        self.leftLayout.itemAt(1).widget().setText(data["Name"])
        self.leftLayout.itemAt(3).widget().setText(str(data["DOB"]))
        self.leftLayout.itemAt(5).widget().setText(data["ResidentialAddress"])
        self.leftLayout.itemAt(7).widget().setText(data["BusinessAddress"])
        self.leftLayout.itemAt(9).widget().setText(str(data["Fee"]))
        self.leftLayout.itemAt(11).widget().setText(str(data["LastPaid"]))
        self.rightLayout.itemAt(1).widget().setText(MemId)
        self.rightLayout.itemAt(3).widget().setText(data["NameSecondary"])
        self.rightLayout.itemAt(5).widget().setText(data["ResidentialNumber"])
        self.rightLayout.itemAt(7).widget().setText(data["BusinessNumber"])
        self.rightLayout.itemAt(9).widget().setText(self.feeKey.get(data["FeeType"],"Undefined"))
        
    
    def setFormInfo(self):
        data = {}
        data["Name"] = self.leftLayout.itemAt(1).widget().text()
        data["DOB"] = datetime.datetime.strptime(self.leftLayout.itemAt(3).widget().text(),"%Y-%m-%d %H:%M:%S")
        data["ResidentialAddress"] = self.leftLayout.itemAt(5).widget().text()
        data["BusinessAddress"] = self.leftLayout.itemAt(7).widget().text()
        data["Fee"] = int(self.leftLayout.itemAt(9).widget().text())
        data["LastPaid"] = datetime.datetime.strptime(self.leftLayout.itemAt(11).widget().text(),"%Y-%m-%d %H:%M:%S")
        data["MemId"] = self.rightLayout.itemAt(1).widget().text()
        data["NameSecondary"] = self.rightLayout.itemAt(3).widget().text()        
        data["ResidentialNumber"] = self.rightLayout.itemAt(5).widget().text()
        data["BusinessNumber"] = self.rightLayout.itemAt(7).widget().text()
        data["FeeType"] = self.feeKeyRev.get((self.rightLayout.itemAt(9).widget().text()))
        self.db.updateInfo(data)
    
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

    lwidget = memberFormWidget(config,db)
    lwidget.getFormInfo("NA")
    window.setCentralWidget(lwidget)
    window.show()

    sys.exit(App.exec_())