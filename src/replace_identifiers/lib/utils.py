import json
import os
import sys


def get_objects_from(json_file=None):
    json_objects = None
    if json_file is not None:
        json_fp = open(json_file, 'r')
        json_objects = json.loads(json_fp.read())
    return json_objects


def verify_paths(data_path):
    for path_name in data_path:
        if not os.path.exists(path_name):
            raise IOError("Please, verify '{}' directory path".format(path_name))


def load_files(file_path):
    all_jsons_data = {}
    for filename in os.listdir(file_path):
        if os.path.isdir(os.path.join(file_path, filename)):
            continue
        with open(os.path.join(file_path, filename), 'r') as fp:
            try:
                json_data = json.loads(fp.read())
            except ValueError as value_error:
                print("{} is not a valid json file. File is being ignored.".format(filename))
                continue
        all_jsons_data[filename] = json_data.copy()
    return all_jsons_data


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
    sys.stdout.write(f"\rReplacing {collection_name} IDs: |{bar}| {percent}% ({current}/{total})")
    sys.stdout.flush()
