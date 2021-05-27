import json
import os
from pymongo import MongoClient
from collections import OrderedDict


def mongodb_connection(mongodb_url, database):
    client = MongoClient(mongodb_url)
    db_conn = client[database]
    return db_conn, client


def mongodb_close(client):
    client.close()


def load_schemas(schemas_path):
    if os.path.isdir(schemas_path) is True:
        for filename in os.listdir(schemas_path):
            if os.path.isdir(os.path.join(schemas_path, filename)):
                continue
            with open(os.path.join(schemas_path, filename), 'r') as schema:
                try:
                    schema = json.loads(schema.read())
                    for collection_name, schema_rules in schema.items():
                        yield collection_name, schema_rules
                except ValueError as value_error:
                    print("{} is not a valid json file. File is being ignored.".format(filename))
                    continue
    else:
        raise NotADirectoryError("{} is not a valid directory, please check the value of -s argument".format(schemas_path))


def set_collection_schema_rules(schema_name, schema_rules):
    schema_rules = [
        ('collMod', schema_name),
        ('validator', schema_rules["validator"]),
        ('validationLevel', schema_rules["validationLevel"]),
        ('validationAction', schema_rules["validationAction"])
    ]
    return OrderedDict(schema_rules)