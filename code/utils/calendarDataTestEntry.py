from datetime import datetime
from datetime import timedelta
from random import randint, sample
from utils.tools import getConfig
from utils.DBManager import DBManager

START = datetime.strptime('1/1/2021 1:01 AM', '%d/%m/%Y %I:%M %p')
END = datetime.strptime('1/12/2022 1:01 AM', '%d/%m/%Y %I:%M %p')
MIN_TIME = datetime.min.time()

def getIds(ids : list) -> list:
    k = randint(8,18)
    return sample(ids,k)

def getDate():
    random_second = 1 * 24 * 60 * 60
    currDate = START + timedelta(seconds=random_second)
    output = datetime.combine(currDate.date(), MIN_TIME)
    return output


config = getConfig()
db = DBManager(config)

ids = db.infoCollection.distinct("MemId")

print(getIds(ids))
