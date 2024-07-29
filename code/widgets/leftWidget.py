# Importing Libraries
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QListWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
)
from widgets.memberListWidget import memberListWidget
from widgets.memberFormWidget import memberFormWidget

# Class Definition


class searchWidget(QWidget):

    def __init__(self, config: dict, db, listWidget):
        super().__init__()
        self.db = db
        self.config = config
        self.listWidget = listWidget
        self.label = QLabel("Member Information")
        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetList)
        self.searchBox = QLineEdit()
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.search)
        self.AddButton = QPushButton("Add New Member")
        self.initLayout()

    def initLayout(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addStretch()
        self.layout.addStretch()
        self.layout.addWidget(self.AddButton)
        self.layout.addWidget(self.resetButton)
        self.layout.addWidget(self.searchBox)
        self.layout.addWidget(self.searchButton)
        self.setLayout(self.layout)

    def search(self):
        text = self.searchBox.text()
        self.db.searchInfo(text)
        items = self.db.getMemberPage(1)
        self.listWidget.emptyList()
        self.listWidget.insertItems(items)

    def resetList(self):
        self.db.getMemberList()
        self.listWidget.displayPage(1)


class pageWidget(QWidget):
    def __init__(self, config: dict, db, listWidget):
        super().__init__()
        self.db = db
        self.config = config
        self.listWidget = listWidget
        self.label = QLabel("Page : 1/" + str(db.getMaxMemberPages()))
        self.nextButton = QPushButton("Next")
        self.nextButton.clicked.connect(self.nextList)
        self.prevButton = QPushButton("Prev")
        self.prevButton.clicked.connect(self.prevList)
        self.initLayout()

    def initLayout(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.prevButton)
        self.layout.addStretch()
        self.layout.addWidget(self.label)
        self.layout.addStretch()
        self.layout.addWidget(self.nextButton)
        self.setLayout(self.layout)

    def nextList(self):
        currPage = self.listWidget.currentPage
        maxPage = self.db.getMaxMemberPages()
        if currPage == maxPage:
            return None
        self.listWidget.displayPage(currPage + 1)
        self.label.setText(f"Page : {currPage+1}/{self.db.getMaxMemberPages()}")
        return None

    def prevList(self) -> None:
        currPage = self.listWidget.currentPage
        if currPage == 1:
            return None
        self.listWidget.displayPage(currPage - 1)
        self.label.setText(f"Page : {currPage-1}/{self.db.getMaxMemberPages()}")
        return None


class leftWidget1(QWidget):

    def __init__(self, config: dict, db):
        super().__init__()
        self.db = db
        self.config = config
        self.listWidget = memberListWidget(config, db)
        self.topWidget = searchWidget(config, db, self.listWidget)
        self.bottomWidget = pageWidget(config, db, self.listWidget)
        self.initLayout()

    def initLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.topWidget)
        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.bottomWidget)
        self.setLayout(self.layout)


class leftWidget(QWidget):

    def __init__(self, config: dict, db):
        super().__init__()
        self.db = db
        self.config = config
        self.recordWidget = leftWidget1(config, db)
        self.formWidget = memberFormWidget(config, db)
        self.initLayout()

    def initLayout(self):
        self.layout = QStackedLayout()
        self.layout.insertWidget(0, self.recordWidget)
        self.recordWidget.listWidget.listWidget.itemDoubleClicked.connect(
            self.callMemberForm
        )
        self.recordWidget.topWidget.AddButton.clicked.connect(self.callNewForm)
        self.layout.insertWidget(1, self.formWidget)
        self.formWidget.backButton.clicked.connect(self.callRecordsPage)
        self.formWidget.submitButton.clicked.connect(self.callRecordsPage)
        self.formWidget.deleteButton.clicked.connect(self.callRecordsPage)
        self.setLayout(self.layout)

    def callMemberForm(self, item):
        self.layout.setCurrentIndex(1)
        MemId = item.text().split(" ")[0]
        self.formWidget.getFormInfo(MemId)

    def callNewForm(self):
        self.layout.setCurrentIndex(1)
        self.formWidget.getFormInfo("NA")

    def callRecordsPage(self):
        self.layout.setCurrentIndex(0)
        self.recordWidget.listWidget.displayPage(1)


if __name__ == "__main__":
    import sys

    sys.path.append("../")
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from widgets.utils.DBManager import DBManager
    from widgets.utils.tools import getConfig

    config = getConfig()

    db = DBManager(config)

    App = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(0, 0, 900, 800)

    lwidget = leftWidget(config, db)
    window.setCentralWidget(lwidget)
    window.show()

    sys.exit(App.exec_())
