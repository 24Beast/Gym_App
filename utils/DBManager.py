# Importing Libraries
from datetime import datetime
from pymongo import MongoClient
from tools import DateToDateTime

'''
Data Dictionary
{ 
MemId: Int
Name : Str,
DOB : DateTime,
NameSecondary : Str,
ResidentialAddress : Str,
ResidentialNumber : Str
BusinessAddress : Str,
BusinessNumber : Str
Fee : Int,
FeeType : Int,
LastPaid : DateTime 
}

Calendar Dictionary
{
Date : Datetime
MemIds : List
}
'''

# Class Definition

class DBManager():
    
    def __init__(self,config):
        self.client = MongoClient(config["clientAddress"])
        self.db = self.client[config["DB"]]
        self.infoCollection = self.db[config["infoCollection"]]
        self.calendarCollection = self.db[config["calendarCollection"]]
        self.MULTIPLIER = config["MULTIPLIER"]
        if(not("MemId_1" in self.infoCollection.index_information())):
            print(self.infoCollection.create_index([('MemId', 1)],unique=True))
        if(not("Date_1" in self.calendarCollection.index_information())):
            print(self.calendarCollection.create_index([('Date', 1)],unique=True))
        
        
    def insertInfo(self, data: dict) -> None:
        self.infoCollection.insert_one(data)
        print(f"Data inserted for MemId : {data['MemId']}")
        

    def updateInfo(self, data: dict) -> None:
        ID = data["MemId"]
        self.infoCollection.find_one_and_replace({"MemId":ID}, data)
        print(f"Updated Values for MemId : {data['MemId']}")
    
    
    def searchInfo(self, string : str) -> list:
        docs = []
        for doc in self.infoCollection.find({"$or":[{"Name":{"$regex":string,"$options":"i"}},
                                                    {"Address":{"$regex":string,"$options":"i"}}]
                                             }):
            docs.append(doc)
        return docs
    
    
    def getMemId(self, name: str) -> int:
        number = (ord(name[0].lower())-ord('a'))*self.MULTIPLIER 
        memNum = number
        for doc in self.infoCollection.find({"MemId": {"$gt": (number-1),"$lt": (number + self.MULTIPLIER)}}).sort("MemId",-1):
            memNum = doc["MemId"] + 1
            print(memNum)
            break
        if(memNum>=(number+self.MULTIPLIER)):
            print(f"ERROR: Member Limit Exceeded, MemId {memNum} may overwrite existing data.")
        return memNum
    
    
    def addCalender(self, date, MemId) -> None:
        if(type(date)!=datetime):
            date = DateToDateTime(date)
        self.calendarCollection.update_one({"Date":date},{"$addToSet":{"MemIds":MemId}})
        print(f"Added MemId : {MemId} to Date : {date}")
    

    def removeCalender(self, date, MemId) -> None:
        if(type(date)!=datetime):
            date = DateToDateTime(date)
        self.calendarCollection.update_one({"Date":date},{"$pull":{"MemIds":MemId}})
        print(f"Removed MemId : {MemId} to Date : {date}")

    
    def fetchCalender(self, MemId) -> list:
        dates = []
        for doc in self.calendarCollection.find({"MemIds":{"$elemMatch":{"$eq":MemId}}}):
            dates.append(doc["Date"])
        return dates



if __name__ == "__main__":
    config = {"clientAddress":"mongodb://localhost:27017/",
              "DB":"TestGymDB",
              "infoCollection":"MemberData",
              "calendarCollection":"CalendarData"
              }
    db = DBManager(config)