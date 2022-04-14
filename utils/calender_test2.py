import time
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from random import randrange

START = datetime.strptime('1/1/2022 1:01 AM', '%d/%m/%Y %I:%M %p')
END = datetime.strptime('1/12/2022 1:01 AM', '%d/%m/%Y %I:%M %p')
MIN_TIME = datetime.min.time()

def randomDate():
    delta = END - START
    random_second = randrange(delta.days) * 24 * 60 * 60
    currDate = START + timedelta(seconds=random_second)
    output = datetime.combine(currDate.date(), MIN_TIME)
    return output

def createEntry(collection) -> dict:
    currDate = randomDate()
    newDate = randomDate()
    data = {"Date1" : currDate,
            "Date2" : newDate
            }
    return data


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_db"]
    collection = db["collection_2"]
    
    
    for i in range(25):
        collection.insert_one(createEntry(collection))
        
    for doc in collection.find({"$expr" :
                                {"$lt" :
                                 [0,
                                  {"dateDiff" : {"startDate" : "$Date2",
                                                 "endDate" : "$Date1",
                                                 "unit" : "month"}
                                   }
                                  ]
                                 }
                                }):
        print(doc)
        
    
    pipeline = [{"$match" :
                 {
                     "$expr" :
                         {
                             "$lte" : [
                                 3,
                                 {"$dateDiff" : {
                                     "startDate" : "$Date1",
                                     "endDate" : "$Date2",
                                     "unit" : "month"
                                     }
                                 }
                                 ]
                         }
                  }
                 }]
    
    for i, doc in enumerate(collection.aggregate(pipeline)):
        print(i,doc)
        