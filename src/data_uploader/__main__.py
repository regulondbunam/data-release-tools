import json
import os
import logging

from data_uploader import arguments
from data_uploader.uploader import Uploader


def get_data(directory):
    collection_data = {}
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            continue
        filename = os.path.join(directory, filename)
        json_data = read_json(filename)
        if json_data:
            collection_name = json_data["collectionName"]
            data = json_data["collectionData"]
            collection_data.setdefault(collection_name, []).extend(data)
    return collection_data


def read_json(filename):
    with open(filename, 'r') as fp:
        try:
            json_data = json.loads(fp.read())
        except ValueError as value_error:
            print("{} is not a valid json file. File is being ignored.".format(filename))
            json_data = {}
    return json_data


def set_log(log_path):
    if not os.path.isdir(log_path):
        raise IOError(
            "{} directory does not exist, please edit your log argument value".format(log_path))
    log_path = os.path.join(log_path, 'data_uploader.log')
    logging.basicConfig(filename=log_path,
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)

    return log_path


def run(connection_url, database, input_path=None):
    mongodb_connection = Uploader(connection_url, database)
    json_data = get_data(input_path)
    for collection_name, json_data in json_data.items():
        for json_object in json_data:
            mongodb_connection.upload_object(collection_name, json_object)


if __name__ == '__main__':
    args = arguments.load()
    log_path = args.log
    mongodb_url = args.url
    database = "regulondbmultigenomic" if args.regulondbmultigenomic else "regulondbdatamarts"

    input_path = args.inputdir
    log_path = set_log(log_path)
    run(mongodb_url, database, input_path)
    print("Process finished, check: {}, for more info".format(log_path))
