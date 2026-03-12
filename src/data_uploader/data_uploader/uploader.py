import logging
from pymongo import MongoClient, errors


class Uploader:
    inconsistencies_generated = False

    def __init__(self, connection_url, database):
        self.client = MongoClient(connection_url)
        self.db_conn = self.client[database]

    def close(self):
        try:
            self.client.close()
        except Exception:
            logging.exception("Error closing MongoClient")

    def upload_object(self, collection_name, json_object):
        if collection_name not in self.db_conn.list_collection_names():
            logging.error("Collection does not exist: %s", collection_name)
            Uploader.inconsistencies_generated = True
            return Uploader.inconsistencies_generated

        collection = self.db_conn[collection_name]

        try:
            collection.insert_one(json_object)
            Uploader.inconsistencies_generated = False

        except errors.DuplicateKeyError as duplicate_error:
            logging.error(
                "Working on collection: %s; object: %s; duplicate key error: %s",
                collection_name, json_object.get("_id"), str(duplicate_error)
            )
            Uploader.inconsistencies_generated = True

        except errors.WriteError as write_error:
            msg = write_error.details.get("errmsg") if write_error.details else str(write_error)
            logging.error(
                "Working on collection: %s; object: %s; write error: %s",
                collection_name, json_object.get("_id"), msg
            )
            Uploader.inconsistencies_generated = True

        except errors.PyMongoError as mongo_error:
            logging.error(
                "Working on collection: %s; object: %s; pymongo error: %s; type: %s",
                collection_name, json_object.get("_id"), str(mongo_error), type(mongo_error).__name__
            )
            Uploader.inconsistencies_generated = True

        except Exception as unexpected_error:
            logging.error(
                "Working on collection: %s; object: %s; unexpected error: %s; type: %s",
                collection_name, json_object.get("_id"), str(unexpected_error), type(unexpected_error).__name__
            )
            Uploader.inconsistencies_generated = True

        return Uploader.inconsistencies_generated
