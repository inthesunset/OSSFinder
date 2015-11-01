
#commits-transfer.py

# Procedure overview:
#- Have a source collection for commits and target collection for commits.
#- Retreive 500 repos at a time, take the url and full_name properties, store them in a dict.
#- Retrieve 500 comits at a time, extract a full_name from the commit. If it matches one
# of the repos, insert it to the target collection.

#- It is not possible to do an $in query here, because the commits only have a url property
# and no full_name property. However, a url can be extracted from the full_name, so that's
# why we iterate over all of the commits.

import pymongo, sys
from pprint import pprint

output = open('commits-transfer.txt', 'w')

client = pymongo.MongoClient (host="da0.eecs.utk.edu")

# Define the source and target collections
repos = client['ossfinder']['repositories']
source = client['test']['commits']
target = client['ossfinder']['commits']

# Create a dict of "full_name" properties for repos
# The full_name is [user]/[repo name] - ex: twbs/bootstrap
repo_full_names = {};

# Clear out the target collection to ensure a clean copy
target.delete_many({})

# Populate the dict
skip = 0
limit = 500
count = 1
while count > 0:
	docs = repos.find({}, {"url": 1, "full_name": 1}).skip(skip).limit(limit);
	docs = list(docs)
	skip += limit
	count = len(docs)
	for doc in docs:
		repo_full_names[doc['full_name']] = 0


# Retrieve and iterate over all commits.
# We only care about the url and the commiter, so we are ignoring other fields. 
# Check the commit's url property to see  if it matches one of the full names.
# If it does, add it to a list that will be inserted to the target collection.
skip = 0
limit = 500
count = 1
total = 0
fields = {"url": 1, "author": 1}
while count > 0:
	try:
		docs = source.find({}, fields).skip(skip).limit(limit)
		docs = list(docs)
		commits_to_insert = []
		# Loop over the docs, extract the url and full_name properties
		# The full_name property comes from the url
		for doc in docs:
			url = doc['url']
			full_name = '/'.join(url.split('/')[4:6]) #comment
			# If we care about this commit's repo, we need to insert it.
			if full_name in repo_full_names:
				doc['full_name'] = full_name
				commits_to_insert.append(doc)
	
		# More efficient to insert a list all at once instead of individually
		if len(commits_to_insert) > 0:
			target.insert_many(commits_to_insert)
	
		count = len(docs)
		skip += limit	
		total += len(commits_to_insert)
		info = str([count,len(commits_to_insert),total])
		output.write(info)
		print(info)			

	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise SystemExit
info = 'COMPLETE: ' + str(total)
output.write(info)
print(info)

