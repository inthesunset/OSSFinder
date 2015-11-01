import sys, re, pymongo

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
repos = client['ossfinder']['repos']

skip = 0
limit = 50
count = 1

while count > 0:
  # Using skip and limit to "chunk" the query, only returning the id and
  # full_name fields.
  result = repos.find({}, {'id': 1, 'full_name': 1}).skip(skip).limit(limit)
  result_list = list(result)
  count = result.count(with_limit_and_skip=True)
  skip += limit
  
  for r in result_list:
    print(r['id'], r['full_name'])


