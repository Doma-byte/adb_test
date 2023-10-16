from abc import ABC, abstractmethod
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class IDatabaseManager(ABC):
    @abstractmethod
    def get_collection(self):
        pass

class DatabaseManager(IDatabaseManager):
    def __init__(self, db_uri):
        try:
            self.db = MongoClient(db_uri)['test_db']
            self.collection_name = self.db['adbrew_test']
        except ConnectionFailure as e:
            logging.error(f'MongoDB connection error: {e}')
            self.collection_name = None

    def get_collection(self):
        return self.collection_name
