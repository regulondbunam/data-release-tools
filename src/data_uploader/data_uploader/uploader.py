import logging

from pymongo import MongoClient
from pymongo import errors


class Uploader(object):
    inconsistencies_generated = False

    def __init__(self, connection_url, database):
        self.client = MongoClient(connection_url)
        self.db_conn = self.client[database]

    def upload_object(self, collection_name, json_object):
        if collection_name in self.db_conn.collection_names():
            collection = self.db_conn[collection_name]
            try:
                collection.insert(json_object)
                logging.info('Working on collection: {}; object: {} loaded correctly'.format(collection_name, json_object["_id"]))
                Uploader.inconsistencies_generated = True

            except errors.DuplicateKeyError as duplicate_key_error:
                '''
                pint(json_object)
                collection.update_one( 
                    {
                        "_id": json_object["_id"]
                    }
                )
                '''
                logging.error('Working on collection: {}; object: {} duplicate key error'.format(collection_name, json_object["_id"]))
                Uploader.inconsistencies_generated = True

            except errors.WriteError as write_error:
                logging.error('Working on collection: {}; object: {}; details: {}'.format(collection_name, json_object["_id"], write_error.details["errmsg"]))
                Uploader.inconsistencies_generated = True

            else:
                Uploader.inconsistencies_generated = False

        return Uploader.inconsistencies_generated

    def upload_json_bulk(self, collection_name, json_bulk):
        if collection_name in self.db_conn.collection_names():
            collection = self.db_conn[collection_name]
            try:
                collection.insert_many(json_bulk)
            except errors.BulkWriteError as bulk_error:
                print(bulk_error)
                print(bulk_error.details)
                raise

    def __del__(self):
        self.client.close()
