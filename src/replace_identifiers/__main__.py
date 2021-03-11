import logging
import os
import json

import identifiers_api

from lib import utils
from lib import arguments
from lib.replace_identifier_object_builder import mg_replace_ids_builder


def create_json(filename, collection_name, collection_data, output_path):
    filename = os.path.join(output_path, filename)
    if not filename.endswith(".json"):
        filename = "{}.json".format(filename)
    with open(filename, 'w') as json_file:
        output_file = {
            "collectionName": collection_name,
            "collectionData": collection_data
        }
        json.dump(output_file, json_file, indent=2, sort_keys=True)


def replace_mg_identifiers(jsons_data, regulondb_version, organism, output_path=None):
    multigenomicdb_identifiers = identifiers_api.regulondbmultigenomic.get_all_identifiers(
        regulondb_version, organism)
    for filename, dataset in jsons_data.items():
        collection_name = dataset.get("collectionName")
        collection_data = dataset.get("collectionData")

        if collection_name not in mg_replace_ids_builder:
            raise NotImplementedError(
                "There's currently no identifier process for the {} collection.\n\t Skipping this collection data".format(collection_name))

        for json_object in collection_data:
            mg_replace_ids_builder[collection_name](
                json_object, multigenomicdb_identifiers, collection_name)

        create_json(filename, collection_name, collection_data, output_path)


def set_log(log_path):
    if not os.path.isdir(log_path):
        raise IOError(
            "{} directory does not exist, please edit your log argument".format(log_path))
    logging.basicConfig(filename=os.path.join(log_path, 'replace_identifiers.log'),
                        format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


def run(regulondb_version, organism, input_path, output_path, database):
    utils.verify_paths([input_path, output_path])
    input_files = utils.load_files(input_path)
    if database == 'regulondbmultigenomic':
        replace_mg_identifiers(
            input_files, regulondb_version, organism, output_path)
    elif database == "regulondbht":
        pass
    elif database == "regulondbdatamarts":
        pass
    else:
        raise KeyError("Process of creating identifiers for the selected "
                       f"database({database}) has not been implemented or "
                       f"there's a typo, please verify it before continuing")


if __name__ == '__main__':
    arguments = arguments.load_arguments()

    set_log(arguments.log)

    identifiers_api.connect(arguments.url)
    run(arguments.version, arguments.organism, arguments.inputdir,
        arguments.outputdir, arguments.database)
