import sys, re, pymongo, json
import requests


jsonDict = {}

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
args = list(sys.argv)
args.pop (0)
db = client [args.pop (0)]
# Reference a particular collection in the database
coll = db [args.pop (0)]

rest = args
for r in coll .find ():  
  if (rest[0] in r and r[rest[0]] is not None):
   n = r[rest[0]]
   for i in range (1, len(rest)):
    if (r[rest[i]] is None): n1 = ''
    else:
     if (type(r[rest[i]]) is int): n1 = str (r[rest[i]])
     else: n1 = r[rest[i]]
    n = n + ';' + n1
   print (n.encode('ascii', errors='ignore'))
