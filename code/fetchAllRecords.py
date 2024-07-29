import pandas as pd
from widgets.utils.DBManager import DBManager
from widgets.utils.tools import getConfig

OUTFILE = "../records.csv"

RETAIN_COLS = ["MemNum", "Name", "NameSecondary", "ResidentialNumber"]

config = getConfig()
db = DBManager(config)

db.getMemberList()

items = []

for num, item in enumerate(db.infoDocs):
    print(f"\rFetching item number {num}", end="")
    item["MemNum"] = db.memNumToMemId(item["MemId"])
    items.append(item)

df = pd.DataFrame.from_records(items)

df = df[RETAIN_COLS]

df.to_csv(OUTFILE, index=False)
