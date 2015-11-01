import sys, re, pymongo
from pprint import pprint

client = pymongo.MongoClient (host="da0.eecs.utk.edu")

# Define the source and target collections
source = client['test']['repos']
target = client['ossfinder']['repositories']

# Query setup
minForks = 20
minWatchers = 20
skip = 0
limit = 500
count = 4
total = 0
query = {"forks": {"$gt": minForks}, "watchers": {"$gt": minWatchers}}
fields = {"_id": 0}

print('watchers: ', minWatchers)
print('forks: ',  minForks)

# Delete any existing records
target.delete_many({})

while count > 1:
	# Get the docs, the count, and convert docs to a python friendly list
	docs = source.find(query, fields).skip(skip).limit(limit)
	
	# Initialize a bulk operation - this is more performant than 
	# individual inserts and allows us to "upsert()", which insert_many()
	# doesn't allow 
	#bulk = target.initialize_ordered_bulk_op()
	#for doc in docs:
	#	bulk.find({'id': doc['id']}).upsert().update({'$set': doc})
		#bulk.insert(doc)
	# Execut the bulk operation
	#bulk_result = bulk.execute()
	#pprint(bulk_result)	

	result = target.insert_many(list(docs))
	#print(result.inserted_ids)
	# Increment values to maintain the loop
	#count = docs.count(with_limit_and_skip=True)
	count = len(result.inserted_ids)
	total += count
	skip += limit

	print(count, total)

