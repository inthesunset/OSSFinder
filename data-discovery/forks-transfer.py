#forks-transfer.py

# Procedure overview:
# - Same as the commits-transfer procedure

import pymongo, sys
from pprint import pprint
import transfer_helpers as helpers

output = open('forks-transfer.txt', 'w')

client = pymongo.MongoClient (host="da0.eecs.utk.edu")

# Define the source and target collections
repos = client['ossfinder']['repositories']
source = client['test']['watchers']
target = client['ossfinder']['watchers']

repo_full_names = helpers.get_repo_full_names(repos);

# Clear out the target collection to ensure a clean copy
target.delete_many({})

skip = 0
limit = 1000
count = 1
total = 0
fields = {"owner": 1, "full_name": 1, "repo": 1, "url": 1}
while count > 0:
	docs = source.find({}, fields).skip(skip).limit(limit)
	docs = list(docs)
	to_insert = []
	for doc in docs:
		# Get the source full name to use for comparison instead
		# of just the full name
		source_full_name = doc['owner'] + '/' + doc['repo']
		if source_full_name in repo_full_names:
			doc['source_full_name'] = source_full_name
			to_insert.append(doc)

	if len(to_insert) > 0:
		target.insert_many(to_insert)
		
	skip += limit
	count = len(docs)
	total += len(to_insert)
	info =str(['forks', count, len(to_insert), total])
	output.write(info)
	print(info)

info = 'COMPLETE: ' + str(total)
output.write(info)
print(info)

