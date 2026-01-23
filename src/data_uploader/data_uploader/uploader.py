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
        if collection_name in self.db_conn.list_collection_names():
            collection = self.db_conn[collection_name]
            try:
                collection.insert_one(json_object)
                logging.info(
                    "Working on collection: %s; object: %s loaded correctly",
                    collection_name, json_object.get("_id")
                )
                print(
                    f'Working on collection: {collection_name}; object: {json_object.get("_id")} loaded correctly',
                    flush=True
                )
                Uploader.inconsistencies_generated = True

            except errors.DuplicateKeyError:
                logging.error(
                    "Working on collection: %s; object: %s duplicate key error",
                    collection_name, json_object.get("_id")
                )
                print(
                    f'Working on collection: {collection_name}; object: {json_object.get("_id")} duplicate key error',
                    flush=True
                )
                Uploader.inconsistencies_generated = True

            except errors.WriteError as write_error:
                msg = write_error.details.get("errmsg") if write_error.details else str(write_error)
                logging.error(
                    "Working on collection: %s; object: %s; details: %s",
                    collection_name, json_object.get("_id"), msg
                )
                print(
                    f'Working on collection: {collection_name}; object: {json_object.get("_id")}; details: {msg}',
                    flush=True
                )
                Uploader.inconsistencies_generated = True

            else:
                Uploader.inconsistencies_generated = False

        return Uploader.inconsistencies_generated
