#issues-transfer.py

# Procedure overview:
# - Same as the commits-transfer procedure

import pymongo,sys
from pprint import pprint
import transfer_helpers as helpers

output = open('issue-comments-transfer.txt', 'w')

client = pymongo.MongoClient (host="da0.eecs.utk.edu")

# Define the source and target collections
repos = client['ossfinder']['repositories']
source = client['test']['issue_comments']
target = client['ossfinder']['issue_comments']

repo_full_names = helpers.get_repo_full_names(repos);

# Clear out the target collection to ensure a clean copy
target.delete_many({})

skip = 0
limit = 1000
count = 1
total = 0
fields = {"user": 1, "url": 1}
while count > 0:
	try:
		docs = source.find({}, fields).skip(skip).limit(limit)
		docs = list(docs)
		to_insert = []
		for doc in docs:
			full_name = helpers.url_to_full_name(doc['url'])
			if full_name in repo_full_names:
				doc['full_name'] = full_name
				to_insert.append(doc)
	
		if len(to_insert) > 0:
			target.insert_many(to_insert)
			
		skip += limit
		count = len(docs)
		total += len(to_insert)
		info = str(['issue comments', count, len(to_insert), total])
		output.write(info)
		print(info)

	except:
                print("Unexpected error:", sys.exc_info()[0])
               	raise SystemExit

info = 'COMPLETE: ' + str(total)
output.write(info)
print(info)
