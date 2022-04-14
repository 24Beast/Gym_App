from datetime import datetime
from PyQt5.QtCore import QDate

MIN_TIME = datetime.min.time()

def DateToDateTime(date):
    return datetime.combine(date, MIN_TIME)

def QDatetoDateTime(date):
    s = date.toString("dd/MM/yyyy")
    return datetime(*[int(i) for i in s.split("/")],0,0)

def DateTimeToQDate(date):
    s = date.strftime("%d/%m/%Y")
    return QDate.fromString(s,"dd/MM/yyyy")