import json
import os


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