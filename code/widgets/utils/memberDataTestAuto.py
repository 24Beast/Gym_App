import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from widgets.utils.DBManager import DBManager
from widgets.utils.tools import getConfig

# Move this file to code folder for it to work

def filterData(dataItem: dict) -> dict :
    dataItem["LastPaid"] = datetime.strptime(dataItem["LastPaid"],"%d/%m/%Y")
    dataItem["DOB"] = datetime.strptime(dataItem["DOB"],"%d/%m/%Y")
    dataItem["DOJ"] = datetime.strptime(dataItem["DOJ"],"%d/%m/%Y")
    dataItem["MemId"] =  "NA"
    return dataItem


if __name__ == "__main__":
    
    with open("../sample_json.json") as f:
        data = json.load(f)["data"]
    
    config = getConfig()

    db = DBManager(config)
    
    for item in data:
        db.insertInfo(filterData(item))
    