
# Iterate over repos, compare each of the repos to all of the
# repos after it.

import pymongo
from pprint import pprint

output = open('commits-output.txt', 'w')

client = pymongo.MongoClient(host="da0.eecs.utk.edu")

# Define source and target collections
repos = client['ossfinder']['repositories']
commits = client['ossfinder']['commits']
relationships = client['ossfinder']['relationships']


# Iterate over repos, one by one
begin_outer = 0
while True:
	docs = repos.find({}).skip(begin_outer).limit(1)
	docs = list(docs)
	begin_outer += 1

	if(len(docs) < 1):
		break

	print(docs[0]['full_name'])

	# Iterate again, this time starting at begin_outer + 1
	begin_inner = begin_outer + 1
	limit_inner = 1000
	while True:
		docs_inner = repos.find({}).skip(begin_inner).limit(limit_inner)
		docs_inner = list(docs_inner)
		begin_inner += limit_inner
		if(len(docs_inner) < 1): break
		print('  ', docs_inner[0]['full_name'])	
		


	
