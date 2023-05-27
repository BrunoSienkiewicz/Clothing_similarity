from pymongo import MongoClient


class Database(object):
    client = MongoClient(
        host = [ 'localhost:27017' ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
    )
    db = client["grailed"]

    def __init__(self, category=None):
        if category:
            self.collection = self.db[category]
        else:
            self.collection = self.db["all"]

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)
    

def main():
    database = Database()
    database.insert({"test": "test"})
    print(database.find({"test": "test"}))


if __name__ == "__main__":
    main()
    