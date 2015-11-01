## module transfer_helpers

# Assumes the url is of format
# https://api.github.com/repos/twbs/bootstrap/etc/etc/etc
def url_to_full_name(url):
	full_name = '/'.join(url.split('/')[4:6])
	return full_name

def get_repo_full_names(repo_collection):
	skip = 0
	limit = 500
	count = 1
	full_names = {}
	while count > 0:
		docs = repo_collection.find({}, {"url": 1, "full_name": 1}).skip(skip).limit(limit)
		docs = list(docs)
		for doc in docs:
			full_names[doc['full_name']] = 0
		skip += limit
		count = len(docs)
	return full_names

