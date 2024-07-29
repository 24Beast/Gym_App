# Importing Libraries
from PyQt5 import QtCore
from widgets.leftWidget import leftWidget
from widgets.rightWidget import rightWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout

# Class Definition


class mainWidget(QWidget):

    def __init__(self, config: dict, db) -> None:
        super().__init__()
        self.db = db
        self.config = config
        self.lWidget = leftWidget(config, db)
        self.rWidget = rightWidget(config, db)
        self.rWidget.setMinimumSize(QtCore.QSize(800, 900))
        self.initLayout()
        self.connectWidgets()

    def initLayout(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.lWidget)
        self.layout.addWidget(self.rWidget)
        self.setLayout(self.layout)

    def connectWidgets(self):
        self.lWidget.formWidget.backButton.clicked.connect(self.refreshCalendar)
        self.lWidget.formWidget.backButton.clicked.connect(self.refreshPending)
        self.lWidget.recordWidget.listWidget.listWidget.itemDoubleClicked.connect(
            self.selectCalendar
        )
        self.rWidget.pendWidget.listWidget.itemDoubleClicked.connect(
            self.showMemberForm
        )

    def refreshCalendar(self):
        self.rWidget.calWidget.refresh_calendar()

    def selectCalendar(self, item):
        MemId = item.text().split(" ")[0]
        self.rWidget.calWidget.getMemberCalendar(MemId)

    def refreshPending(self):
        self.rWidget.pendWidget.displayPending()

    def showMemberForm(self, item):
        self.lWidget.layout.setCurrentIndex(1)
        MemId = item.text().split("\t")[0]
        self.lWidget.formWidget.getFormInfo(MemId)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from widgets.utils.DBManager import DBManager
    from widgets.utils.tools import getConfig

    config = getConfig()
    db = DBManager(config)

    App = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(0, 0, 1600, 900)
    window.setWindowTitle(config["title"])

    stylesheet = "style.qss"
    with open(stylesheet, "r") as fh:
        App.setStyleSheet(fh.read())

    widget = mainWidget(config, db)
    window.setCentralWidget(widget)
    window.show()

    sys.exit(App.exec_())
