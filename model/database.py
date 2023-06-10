from pymongo import MongoClient
import pandas as pd
import gridfs
from PIL import Image
import io


def retrieve_and_display_image(db, filename):
    im = Image.open(io.BytesIO(db.fs.get_last_version(filename).read()))
    im.show()


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
    

class ImageDatabase(Database):
    def __init__(self, db=None, collection=None):
        super().__init__(db, collection)
        self.fs = gridfs.GridFS(self.db, collection=collection)
    
    def insert(self, image, filename):
        if self.fs.find_one({"filename": filename}):
            return

        with open(image, "rb") as f:
            self.fs.put(f, filename=filename)

    def insert_binary(self, binary, filename):
        if self.fs.find_one({"filename": filename}):
            return

        self.fs.put(binary, filename=filename)
    
    def find(self, query):
        return self.collection.find(query)
    
    def load_image(self, filename):
        return io.BytesIO(self.fs.get_last_version(filename).read())
    
    def load_images(self, filenames):
        return [self.load_image(filename) for filename in filenames]
    

def main():
    database = Database()
    database.insert({"test": "test"})
    print(database.find({"test": "test"}))


if __name__ == "__main__":
    main()
    