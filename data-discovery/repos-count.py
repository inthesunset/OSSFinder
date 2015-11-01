import sys, re, pymongo

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['test']
repos = db['repos']

minForks = 25
minWatchers = 25

skip = 0
limit = 100
count = 4
total = 0

query = {"forks": {"$gt": minForks}, "watchers": {"$gt": minWatchers}}
fields = {"_id": 0, "id": 1, "forks": 1, "watchers": 1}

print('watchers: ', minWatchers)
print('forks: ',  minForks)

while count > 1:
	count = repos.find(query, fields).skip(skip).limit(limit).count(with_limit_and_skip=True)
	total += count
	skip += limit
	print(total)
