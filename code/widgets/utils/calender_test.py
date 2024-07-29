from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from random import randint, randrange

START = datetime.strptime("1/1/2022 1:01 AM", "%d/%m/%Y %I:%M %p")
END = datetime.strptime("1/4/2022 1:01 AM", "%d/%m/%Y %I:%M %p")
MAX_IDS = 1000
MIN_TIME = datetime.min.time()


def randomDate():
    delta = END - START
    random_second = randrange(delta.days) * 24 * 60 * 60
    currDate = START + timedelta(seconds=random_second)
    output = datetime.combine(currDate.date(), MIN_TIME)
    return output


def randomMemId():
    return randint(0, 1000)


def createEntry(collection) -> dict:
    memIds = [randomMemId() for i in range(randint(1, MAX_IDS))]
    currDate = randomDate()
    data = {"Date": currDate, "MemIds": memIds}
    return data


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_db"]
    collection = db["collection_1"]

    # print(collection.create_index([('Date', 1)],unique=True))

    # for i in range(25):
    #     collection.insert_one(createEntry(collection))

    for doc in collection.find({"MemIds": {"$elemMatch": {"$eq": 42}}}):
        print(doc["Date"])
