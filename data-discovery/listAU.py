import sys, re, pymongo, json
import requests


jsonDict = {}
args = list(sys.argv)
args.pop (0)

client = pymongo.MongoClient (host="da0.eecs.utk.edu")
# Get a reference to a particular database
db = client [args.pop(0)]
# Reference a particular collection in the database
coll = db [args.pop(0)]

rest = args

for r in coll .find ({}):
 if rest[0] in r:
  n = r[rest[0]]
  for el in n:
   n1 = el[rest[1]]
   for i in range (2, len(rest)):
    if (rest[i] in el):
     if (rest[i] == 'description' and el[rest[i]] is not None):
      n2 = el[rest[i]]
      n1 = n1 + ';' + n2
     else: n1 = n1 + ';' + str(el[rest[i]])
    else:
     n1 = n1 + ';'
     #sys.stderr.write ("No " + rest[i] + '\n')
   print (n1.encode('ascii', errors='ignore'))

