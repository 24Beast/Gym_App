from datetime import datetime
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate
from PyQT5.QtCore.Qt import AlignCenter
from PyQt5.QtWidgets import QListWidgetItem

MIN_TIME = datetime.min.time()

def DateToDateTime(date):
    return datetime.combine(date, MIN_TIME)

def QDatetoDateTime(date):
    s = date.toString("dd/MM/yyyy")
    return datetime(*[int(i) for i in s.split("/")],0,0)

def DateTimeToQDate(date):
    s = date.strftime("%d/%m/%Y")
    return QDate.fromString(s,"dd/MM/yyyy")

def memberDataToListItem(data : dict, color = "grey"):
    item = QListWidgetItem()
    item.setTextAlignment(AlignCenter)
    text = f"{data['MemId']} \t {data['Name']} \t {data['Number']}"
    item.setBackground(QColor(color))
    item.setText(text)
    return item