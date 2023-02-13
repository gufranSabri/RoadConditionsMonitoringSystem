import pymongo

USER_COLLECTION = "AuthorizedUser"
ROAD_POINT_COLLECTION = "RoadPoints"

client = pymongo.MongoClient("mongodb+srv://gufran:pleasedontsteal@cluster0.w7ri1.mongodb.net/RoadCapture?retryWrites=true&w=majority")
db = client.RoadCapture

def create_collection(collection_name):
    db.create_collection(collection_name)

def insert_data(collection_name, data):
    db[collection_name].insert_one(data)

def insert_many_data(collection_name, data):
    db[collection_name].insert_many(data)

def get_data(collection_name):
    return db[collection_name].find()

def get_data_by_id(collection_name, id):
    return db[collection_name].find_one({"_id": id})

def update_data(collection_name, id, data):
    db[collection_name].update_one({"_id": id}, {"$set": data})

def delete_data(collection_name, id):
    db[collection_name].delete_one({"_id": id})

def delete_all_data(collection_name):
    db[collection_name].delete_many({})