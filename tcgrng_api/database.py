import uuid
import os
from pymongo import MongoClient, ReturnDocument


class Database(object):
    def __init__(self,
                 host=os.environ.get("DB_PORT_27017_TCP_ADDR", "localhost"),
                 port=int(os.environ.get("DB_PORT_27017_TCP_PORT", 27017))):
        self.client = MongoClient(host, port)
        self.db = self.client.db

    def save(self, model):
        if not getattr(model, "_id", None):
            model._id = uuid.uuid4()

        bson = self.db[model._collection].find_one_and_replace(
            {"_id": model._id},
            model.json(),
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return model.__class__(**bson)

    def get_by_id(self, cls, _id):
        return self.get(cls, {"_id": _id})

    def get(self, cls, query):
        bson = self.db[cls._collection].find_one(query)

        if not bson:
            return None

        return cls(**bson)
