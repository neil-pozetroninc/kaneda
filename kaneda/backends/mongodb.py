from __future__ import absolute_import

from datetime import datetime

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

from kaneda.exceptions import ImproperlyConfigured

from .base import BaseBackend


class MongoBackend(BaseBackend):
    """
    MongoDB backend.

    :param db_name: name of the MongoDB database.
    :param collection_name: name of the MongoDB collection used to store metric data.
    :param host: server host.
    :param port: server port.
    :param username: auth username.
    :param password: auth password.
    """
    def __init__(self, db_name, collection_name, host, port, username, password):
        if not MongoClient:
            raise ImproperlyConfigured('You need to install the pymongo library to use the MongoDB backend.')        
        client = MongoClient(host=host, port=port)
        db = client[db_name]
        self.collection = db[collection_name]

    def _get_payload(self, name, value, metric, tags, id_):
        payload = super(MongoBackend, self)._get_payload(name, value, tags)
        payload['timestamp'] = datetime.utcnow()
        payload['metric'] = metric
        if id_:
            payload['_id'] = id_
        return payload

    def report(self, name, metric, value, tags, id_):
        payload = self._get_payload(name, value, metric, tags, id_)
        self.collection.insert_one(payload)