import random
from pymongo import MongoClient

NAMES = ["Addison Rollins", "Jeff Vang", "Aydin Almond", "Mahdi Ramsey", "Jia Avila", "Atlanta Randall", 
"Jacqueline Peralta", "Reid Mackenzie", "Nikkita Benson", "Arabella Kramer", "Diego Nelson", "Fraya Fox",
"Aiyla Atkins", "Gia Copeland", "Zena Hoffman" ,"Donovan Robles", "Mehdi Enriquez", "Lemar Miles" , "Anais Wooten",
"Caspian Sweet", "Subhaan Graves", "Kaine Monaghan", "Cole Little", "Saffa Davidson", "Montgomery Trujillo"]

ADDRESS = """Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium
optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis
obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam
nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,
tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit,
quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos 
sapiente officiis modi at sunt excepturi expedita sint?"""

MIN_ADDR_SIZE = 25

FEE_OPTIONS = [1,3,6,12]

MULTIPLIER = 10**3

def getMemId(name: str, collection) -> int:
    number = (ord(name[0].lower())-ord('a'))*MULTIPLIER 
    memNum = number
    for doc in collection.find({"MemId": {"$gt": (number-1),"$lt": (number + MULTIPLIER)}}).sort("MemId",-1):
        memNum = doc["MemId"] + 1
        print(memNum)
        break
    if(memNum>=(number+MULTIPLIER)):
        print(f"ERROR: Member Limit Exceeded, MemId {memNum} may overwrite existing data.")
    return memNum

def createEntry(name: str,collection) -> dict:
    start = random.randint(0,len(ADDRESS)-MIN_ADDR_SIZE)
    end = random.randint(start+MIN_ADDR_SIZE,len(ADDRESS))
    address = ADDRESS[start:end]
    feeType = random.choice(FEE_OPTIONS)
    fees = random.randint(800,1000)
    memId = getMemId(name,collection)
    data = {"Name": name,
            "Address": address,
            "FeeType": feeType,
            "MemId": memId,
            "Fees": fees
            }
    return data

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_db"]
    collection = db["collection_0"]
    
    #print(collection.create_index([('MemId', pymongo.ASCENDING)],unique=True))
    
    # for name in NAMES:
    #     collection.insert_one(createEntry(name,collection))
    
    matchString = "SinT"
    for doc in collection.find({"$or":[{"Name":{"$regex":matchString,"$options":"i"}},{"Address":{"$regex":matchString,"$options":"i"}}]}):
        print((doc["MemId"],doc["Name"],doc["Address"]))