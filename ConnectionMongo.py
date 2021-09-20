from pymongo import MongoClient
from pprint import pprint 

client = MongoClient("mongodb://Maxence:<password>@cluster0-shard-00-00.srkjc.mongodb.net:27017,cluster0-shard-00-01.srkjc.mongodb.net:27017,cluster0-shard-00-02.srkjc.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-zbmmvx-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.test

collection = db.test_collection # or collection = db['test-collection']

result = collection.insert_one({
    "name": "Tyrion",
    "age": 25
})

print('_id:', result.inserted_id)

collection.insert_one({
    "name": "Daenerys",
    "age": 17
})


# read data
cursors = collection.find({})
for element in cursors:
    pprint(element)

# or get all data response in ram
cursors = collection.find({})
my_result = list(cursors)
pprint(my_result)