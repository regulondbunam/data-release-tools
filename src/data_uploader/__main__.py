import json
import os
import logging

from data_uploader import arguments
from data_uploader.uploader import Uploader


def read_json(filename):
    with open(filename, 'r') as fp:
        try:
            return json.loads(fp.read())
        except ValueError:
            print(f"{filename} is not a valid json file. File is being ignored.", flush=True)
            return {}


def set_log(log_path):
    if not os.path.isdir(log_path):
        raise IOError(f"{log_path} directory does not exist, please edit your log argument value")
    log_path = os.path.join(log_path, 'data_uploader.log')
    logging.basicConfig(
        filename=log_path,
        format='%(levelname)s - %(asctime)s - %(message)s',
        filemode='w',
        level=logging.INFO
    )
    return log_path


def run(connection_url, database, input_path=None):
    mongodb_connection = Uploader(connection_url, database)
    try:
        for filename in os.listdir(input_path):
            full_path = os.path.join(input_path, filename)
            if os.path.isdir(full_path):
                continue
            if not filename.lower().endswith(".json"):
                continue

            json_data = read_json(full_path)
            if not json_data:
                continue

            collection_name = json_data["collectionName"]
            data = json_data["collectionData"]

            logging.info('Working on collection: %s', collection_name)
            print(f'Working on collection: {collection_name}', flush=True)

            for json_object in data:
                mongodb_connection.upload_object(collection_name, json_object)
    finally:
        # clave: cerrar explícitamente ANTES del shutdown del intérprete
        mongodb_connection.close()


if __name__ == '__main__':
    args = arguments.load()
    log_path = set_log(args.log)

    run(args.url, args.database, args.inputdir)

    print(f"Process finished, check: {log_path}, for more info", flush=True)
    print("end", flush=True)

    # opcional pero recomendable: fuerza cierre de handlers de logging
    logging.shutdown()
