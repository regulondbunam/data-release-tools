import json
import os
import logging
import sys


def set_log(log_path):
    if not os.path.isdir(log_path):
        raise IOError("{} directory does not exist, please edit your log argument".format(log_path))
    logging.basicConfig(filename=os.path.join(log_path, 'create_identifiers.log'), format='%(levelname)s - %(asctime)s - %(message)s', filemode='w', level=logging.INFO)


def get_objects_from(json_file=None):
    json_objects = None
    if json_file is not None:
        json_fp = open(json_file, 'r')
        json_objects = json.loads(json_fp.read())
    return json_objects


def verify_paths(data_path):
    if not os.path.exists(data_path):
        raise IOError("Please, verify '{}' directory path".format(data_path))


def load_files(files_path):
    all_jsons_data = []
    for filename in os.listdir(files_path):
        if os.path.isdir(os.path.join(files_path, filename)):
            continue
        with open(os.path.join(files_path, filename), 'r') as fp:
            try:
                json_data = json.loads(fp.read())
            except ValueError as value_error:
                print(
                    "{} is not a valid json file. File is being ignored.".format(
                        filename))
                continue
        all_jsons_data.append(json_data.copy())
    return all_jsons_data


def references_collections_not_listed(jsons_data, is_multigenomic):
    """
    Prints all the reference entities that are not listed in the input data. To let know this to
    the user is of paramount importance. This is only triggered if the process if for the multigenomic database.
    :param jsons_data:
    :param is_multigenomic:
    :return:
    """
    reference_not_listed = verify_reference_collections(jsons_data)
    if is_multigenomic:
        for not_listed_reference_collection in reference_not_listed:
            print("{} data is not presented in the input data, inconsistencies might be presented".format(
                not_listed_reference_collection
            ))


def validate_collection(collection_name, object_builder):
    if collection_name not in object_builder:
        raise NotImplementedError("There's currently no identifier process for the {} collection.\n\t Skipping this collection data".format(collection_name))


def verify_reference_collections(collection_names):
    """
    Verifies if the input data has publication, externalCrossReference and evidence data files. Since the objects
    have references to these entities and everything is mapped through identifiers, if the input data has no reference files
    inconsistencies might be presented.
    :param collection_names:
    :return:
    """
    reference_collections = ["publication", "externalCrossReference", "evidence"]
    for reference_collection_name in reference_collections:
        if reference_collection_name not in collection_names:
            yield reference_collection_name


def print_progress(current, total, collection_name, bar_length=40):
    """
    Displays a real-time progress bar in the console, updating on the same line.

    This function calculates the completion fraction, generates a visual progress
    bar using block characters, and outputs the progress percentage and current
    count relative to the total.

    Args:
        current (int): The number of items currently processed.
        total (int): The total number of items to be processed.
        collection_name (str): The name of the collection or process being tracked.
        bar_length (int, optional): The fixed length of the progress bar display.
                                    Defaults to 40.

    Returns:
        None: The function only performs output to stdout.
    """
    fraction = current / total if total else 1
    filled = int(bar_length * fraction)
    bar = "█" * filled + "-" * (bar_length - filled)
    percent = int(fraction * 100)
    sys.stdout.write(f"\rGenerating {collection_name} IDs: |{bar}| {percent}% ({current}/{total})")
    sys.stdout.flush()
