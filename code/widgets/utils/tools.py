import json
from datetime import datetime
from PyQt5.QtGui import QColor
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QListWidgetItem, QTableWidgetItem

MIN_TIME = datetime.min.time()
PENDING_COLS = ["ID","Name","FeeType","LastPaid"]
FEE_TYPES = {1:"Monthly",3:"Quaterly",6:"Half-Yearly",12:"Yearly"}

def getConfig():
    with open("../config.json","r") as f:
        config = json.load(f)
    return config


def DateToDateTime(date):
    return datetime.combine(date, MIN_TIME)


def QDatetoDateTime(date):
    s = date.toString("dd/MM/yyyy")
    return datetime(*[int(i) for i in s.split("/")][::-1],0,0)


def DateTimeToQDate(date):
    s = date.strftime("%d/%m/%Y")
    return QDate.fromString(s,"dd/MM/yyyy")


def memberDataToListItem(data : dict, config = {"color1" : "grey"}):
    item = QListWidgetItem()
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    text = f"{data['ID']} \t\t {data['Name']} \t\t {data['ResidentialNumber']}"
    item.setBackground(QColor(config["color1"]))
    item.setText(text)
    return item

def pendingDataToTableItems(data : dict, config = {"color1" : "grey"}):
    items = [QTableWidgetItem() for i in range(len(PENDING_COLS))]
    for i,col in enumerate(PENDING_COLS):
        if(col=="FeeType"):
            text = str(FEE_TYPES[data['FeeType']])
        elif(col=="LastPaid"):
            text = str(data['LastPaid'].date())
        else:
            text = str(data[col])
        items[i].setBackground(QColor(config["color1"]))
        items[i].setText(text)
        items[i].setTextAlignment(QtCore.Qt.AlignCenter)
    return items
