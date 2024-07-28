from pymongo import MongoClient
from random import randint, choice, randrange
from datetime import datetime, timedelta

"""
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
"""

NAMES = [
    "Bhanu Tokas",
    "Dharam Singh Tokas",
    "Yogita Tokas",
    "Tushar Tokas",
    "Akhil Menon",
    "Satwik Bhardwaj",
    "Rahul Agarwal",
    "Rohit Jakinapalli",
    "Urvish Chokshi",
    "Lakshay Sood",
    "Geetansh Kumar",
    "Ansh Riyal",
    "Ritvik Nagpal",
    "Sachin Jeph",
    "Vaibhav Beriwal",
    "Sarthak Arora",
    "Nikunj Madan",
    "Leo Adlakha",
    "David Warner",
    "Sachin Tendulkar",
    "Akash Dhiman",
    "Ashutosh Verma",
    "Aryan Ganjoo",
    "Harsh Kataria",
    "Pranav Kataria",
    "Jasbir Kataria",
]

ADDRESS = """Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,
molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum
numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium
optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis
obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam
nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,
tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit,
quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos 
sapiente officiis modi at sunt excepturi expedita sint?"""

MULTIPLIER = 10**4
MIN_ADDR_SIZE = 25
FEE_OPTIONS = [1, 3, 6, 12]

START1 = datetime.strptime("1/1/2022 1:01 AM", "%d/%m/%Y %I:%M %p")
END1 = datetime.strptime("1/4/2022 1:01 AM", "%d/%m/%Y %I:%M %p")

START2 = datetime.strptime("1/1/1970 1:01 AM", "%d/%m/%Y %I:%M %p")
END2 = datetime.strptime("1/12/2000 1:01 AM", "%d/%m/%Y %I:%M %p")
MIN_TIME = datetime.min.time()


def randomDate1():
    delta = END1 - START1
    random_second = randrange(delta.days) * 24 * 60 * 60
    currDate = START1 + timedelta(seconds=random_second)
    output = datetime.combine(currDate.date(), MIN_TIME)
    return output


def randomDate2():
    delta = END2 - START2
    random_second = randrange(delta.days) * 24 * 60 * 60
    currDate = START1 + timedelta(seconds=random_second)
    output = datetime.combine(currDate.date(), MIN_TIME)
    return output


def getMemId(name: str, collection) -> int:
    number = (ord(name[0].lower()) - ord("a")) * MULTIPLIER
    memNum = number
    for doc in collection.find(
        {"MemId": {"$gt": (number - 1), "$lt": (number + MULTIPLIER)}}
    ).sort("MemId", -1):
        memNum = doc["MemId"] + 1
        print(memNum)
        break
    if memNum >= (number + MULTIPLIER):
        print(
            f"ERROR: Member Limit Exceeded, MemId {memNum} may overwrite existing data."
        )
    return memNum


def createEntry(name: str, collection) -> dict:
    start = randint(0, len(ADDRESS) - MIN_ADDR_SIZE)
    end = randint(start + MIN_ADDR_SIZE, len(ADDRESS))
    address1 = ADDRESS[start:end]
    start = randint(0, len(ADDRESS) - MIN_ADDR_SIZE)
    end = randint(start + MIN_ADDR_SIZE, len(ADDRESS))
    address2 = ADDRESS[start:end]
    feeType = choice(FEE_OPTIONS)
    fees = randint(800, 1000)
    lastPaid = randomDate1()
    DOB = randomDate2()
    memId = getMemId(name, collection)
    data = {
        "MemId": memId,
        "Name": name,
        "DOB": DOB,
        "NameSecondary": choice(NAMES),
        "ResidentialAddress": address1,
        "ResidentialNumber": "+91" + str(randint(9 * (10**10), 10**11)),
        "BusinessAddress": address2,
        "BusinessNumber": "+91" + str(randint(9 * (10**10), 10**11)),
        "Fee": fees,
        "FeeType": feeType,
        "LastPaid": lastPaid,
    }
    return data


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["TestGymDB"]
    collection = db["MemberData"]

    print(collection.create_index([("MemId", 1)], unique=True))

    for name in NAMES:
        collection.insert_one(createEntry(name, collection))
