# Importing Libraries
from math import log10, ceil
from datetime import datetime
from pymongo import MongoClient
from widgets.utils.tools import DateToDateTime, memberDataToListItem, pendingDataToListItem


'''
Data Structure Info
-------------------

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
        self.itemsPerPage = config["itemsPerPage"]
        self.numLen = log10(self.MULTIPLIER)
        self.infoDocs = None
        if(not("MemId_1" in self.infoCollection.index_information())):
            print(self.infoCollection.create_index([('MemId', 1)],unique=True))
        if(not("Date_1" in self.calendarCollection.index_information())):
            print(self.calendarCollection.create_index([('Date', 1)],unique=True))

        
    def insertInfo(self, data: dict) -> None:
        if(data["MemId"] == "NA"):
            data["MemId"] = self.getMemNum(data["Name"])
        self.infoCollection.insert_one(data)
        print(f"Data inserted for MemId : {data['MemId']}")
        

    def updateInfo(self, data: dict) -> None:
        if(data["MemId"]=="NA"):
            self.insertInfo(data)
            return
        ID = self.memIdToMemNum(data["MemId"])
        data["MemId"] = ID
        self.infoCollection.find_one_and_replace({"MemId":ID}, data, upsert=True)
        print(f"Updated Values for MemId : {data['MemId']}")
    
    
    def searchInfo(self, string : str) -> None:
        memNum = self.memIdToMemNum(string)
        self.infoDocs =  self.infoCollection.find({"$or":[{"MemId":{"$regex":str(memNum),"$options":"i"}},
                                                    {"Name":{"$regex":string,"$options":"i"}},
                                                    {"NameSecondary":{"$regex":string,"$options":"i"}},
                                                    {"ResidentialAddress":{"$regex":string,"$options":"i"}},
                                                    {"ResidentialNumber":{"$regex":string,"$options":"i"}},
                                                    {"BusinessAddress":{"$regex":string,"$options":"i"}},
                                                    {"BusinessNumber":{"$regex":string,"$options":"i"}},
                                                    ]
                                             })
    
    def getMemberInfo(self, MemId : str):
        memNum = self.memIdToMemNum(MemId)
        for item in self.infoCollection.find({"MemId":memNum}):
            return item
    
    
    def getMemberList(self) -> None:
        self.infoDocs = self.infoCollection.find({}).sort("MemId")
        
    
    def getMaxMemberPages(self) -> int:
        numDocs = len(list(self.infoDocs.clone()))
        numPages = ceil(numDocs/self.itemsPerPage)
        return numPages
    
    
    def getMemberPage(self, page : int):
        items = []
        lower = (page-1)*self.itemsPerPage
        upper = page*self.itemsPerPage
        if(self.infoDocs == None):
            self.getMemberList()
        for i, doc in enumerate(self.infoDocs,start=1):
            if(lower<i<=upper):
                doc["ID"] = self.memNumToMemId(doc["MemId"])
                items.append(memberDataToListItem(doc))
            elif(i>upper):
                break
        self.infoDocs.rewind()
        return items


    def checkDueFees(self) -> list:
        docs = []
        today = datetime.today()
        matches = self.infoCollection.aggregate([{
            "$match" : {
                "$expr" : {
                    "$lt" : [
                        "$FeeType",
                        {"$dateDiff" : {
                            "startDate" : "$LastPaid",
                            "endDate" : today,
                            "unit" : "month"
                            }
                         } 
                        ]
                    }
                }
            },
            {
            "$sort" : {"LastPaid" : 1}
            }
            ])
        for doc in matches:
            doc["ID"] = self.memNumToMemId(doc["MemId"])
            docs.append(pendingDataToListItem(doc))
        return docs
        
    
    def getMemNum(self, name: str) -> int:
        number = (ord(name[0].upper())-ord('A'))*self.MULTIPLIER 
        memNum = number
        for doc in self.infoCollection.find({"MemId": {"$gt": (number-1),"$lt": (number + self.MULTIPLIER)}}).sort("MemId",-1):
            memNum = doc["MemId"] + 1
            print(memNum)
            break
        if(memNum>=(number+self.MULTIPLIER)):
            print(f"ERROR: Member Limit Exceeded, MemId {memNum} may overwrite existing data.")
        return memNum
    
    
    def memNumToMemId(self, memNum : int) -> str:
        alphabet = chr(int(memNum/self.MULTIPLIER) + ord("A"))
        number = str(memNum%self.MULTIPLIER).zfill(int(self.numLen)) 
        return alphabet+number
    
    
    def memIdToMemNum(self, memId: str) -> int:
        if(not(memId[0].isalpha()) or not(memId[1:].isdigit())):
            return -1
        number1 = (ord(memId[0].upper())-ord('A'))*self.MULTIPLIER
        number2 = int(memId[1:])
        return number1 + number2
    
    
    def addCalendar(self, date, MemId) -> None:
        MemNum = self.memIdToMemNum(MemId)
        if(type(date)!=datetime):
            date = DateToDateTime(date)
        if(self.calendarCollection.find_one({"Date":date})==None):
            self.calendarCollection.insert_one({"Date":date,"MemIds":[]})
        self.calendarCollection.update_one({"Date":date},{"$addToSet":{"MemIds":MemNum}})
        print(f"Added MemId : {MemNum} to Date : {date}")
    

    def removeCalendar(self, date, MemId) -> None:
        MemNum = self.memIdToMemNum(MemId)
        if(type(date)!=datetime):
            date = DateToDateTime(date)
        self.calendarCollection.update_one({"Date":date},{"$pull":{"MemIds":MemNum}})
        print(f"Removed MemId : {MemNum} to Date : {date}")

    
    def fetchCalender(self, MemId) -> list:
        MemNum = self.memIdToMemNum(MemId)
        dates = []
        for doc in self.calendarCollection.find({"MemIds":{"$elemMatch":{"$eq":MemNum}}}):
            dates.append(doc["Date"])
        return dates



if __name__ == "__main__":
    from utils.tools import getConfig
    
    config = getConfig()
    db = DBManager(config)