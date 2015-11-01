import sys, re, pymongo

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['test']

stats = db.command("collstats", "repos")

size = (stats['size']) / (1024 * 1024 * 1024)

print(size)



