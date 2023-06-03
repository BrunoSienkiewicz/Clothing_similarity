from pymongo import MongoClient
import pandas as pd


class Database(object):
    client = MongoClient(
        host = [ 'localhost:27017' ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
    )

    def __init__(self, db=None ,collection=None):
        """Initialize the database object."""
        if db:
            self.db = self.client[db]
        else:
            self.db = self.client["test"]

        if collection:
            self.collection = self.db[collection]
        else:
            self.collection = self.db["all"]

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)
    
    def load_as_df(self):
        return pd.DataFrame(list(self.collection.find()))
    

def main():
    database = Database()
    database.insert({"test": "test"})
    print(database.find({"test": "test"}))


if __name__ == "__main__":
    main()
    