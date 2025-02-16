from pymongo import MongoClient
from .envConfig import MongoConfig


class MongoDBHandler:
    _instance = None  # Class-level variable to store the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBHandler, cls).__new__(cls)
            cls._instance.client = MongoClient(MongoConfig.MONGO_CONNECTION_URL)
            cls._instance.db = cls._instance.client[MongoConfig.MONGO_DB_NAME]
        return cls._instance

    def insert_data(self, collection_name, data):
        collection_instance = self.db[collection_name]
        if isinstance(data, list):
            result = collection_instance.insert_many(data)
            return result.inserted_ids
        else:  # Insert a single document
            result = collection_instance.insert_one(data)
            return result.inserted_id

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close_connection(self):

        self.client.close()
