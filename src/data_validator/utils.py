import json
import os
import jsonschema
import sys


def remove_id_pattern_from_schema(schema):
    schema = delete_keys_from_dict(
        schema, ["pattern"], "^RDB[A-Z]{8}[0-9]{5}$")
    schema = delete_keys_from_dict(
        schema, ["pattern"], "^RDM[A-Z]{8}[0-9]{5}$")
    return schema


def delete_keys_from_dict(dictionary_to_update, keys_to_remove, value):
    """
    Delete the keys presented in the keys_to_remove from the dictionary_to_update.
    Loops recursively over nested dictionaries.
    """
    new_dictionary_to_update = dictionary_to_update.copy()
    if type(keys_to_remove) is not set:
        keys_to_remove = set(keys_to_remove)
    for k, v in dictionary_to_update.items():
        if k in keys_to_remove:
            if dictionary_to_update[k] == value:
                new_dictionary_to_update.pop(k)
        if isinstance(v, dict):
            new_dictionary_to_update[k] = delete_keys_from_dict(
                new_dictionary_to_update[k], keys_to_remove, value)
    return new_dictionary_to_update


def verify_paths(data_path):
    for path_name, path in data_path.items():
        if not os.path.exists(path):
            raise IOError(f"Please, verify '{path_name}' directory path")


def _load_files(file_path):
    for filename in os.listdir(file_path):
        if os.path.isdir(os.path.join(file_path, filename)):
            continue
        with open(os.path.join(file_path, filename), 'r') as fp:
            try:
                json_data = json.loads(fp.read())
            except ValueError as value_error:
                print(f"{filename} is not a valid json file. File is being ignored.")
                continue
        yield filename, json_data


def load_schemas(file_path, remove_id_pattern):
    files = {}
    json_schemas = _load_files(file_path)
    for filename, json_schema in json_schemas:
        if remove_id_pattern:
            new_json_schema = remove_id_pattern_from_schema(json_schema)
            for collection_name, values in new_json_schema.items():
                files[collection_name] = values
        else:
            for collection_name, values in json_schema.items():
                files[collection_name] = values
    return files


def load_jsons(file_path):
    files = {}
    jsons_files = _load_files(file_path)
    for filename, json_data in jsons_files:
        files[filename] = json_data
    return files


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
    sys.stdout.write(f"\rValidating {collection_name}: |{bar}| {percent}% ({current}/{total})")
    sys.stdout.flush()


# TODO: Implementar logica para atrapar todos los errores de un json
def validate_data(collection_schema, filename, json_data, valid_data_path, invalid_data_path, error_log_path):
    valid_data = []
    invalid_data = []
    error_log = []
    collection_data = json_data["collectionData"]
    collection_name = json_data["collectionName"]
    total_objects = len(list(collection_data))
    processed = 0
    valid_processed = 0
    invalid_processed = 0
    for current_object in collection_data:
        try:
            jsonschema.validate(instance=current_object, schema=collection_schema["validator"]["$jsonSchema"],
                                format_checker=jsonschema.draft4_format_checker)
            valid_data.append(current_object.copy())
            valid_processed += 1
        except jsonschema.exceptions.ValidationError as validation_error:
            invalid_data.append(current_object.copy())
            error_log.append([current_object["_id"], validation_error.message, [
                             element for element in validation_error.path]])
            invalid_processed += 1
        processed += 1
        print_progress(
            current=processed,
            total=total_objects,
            collection_name=collection_name
        )
    print(f"\n\tValid objects: {valid_processed}\tInvalid: {invalid_processed}")

    if valid_data:
        json_data["collectionData"] = valid_data
        create_json(json_data, os.path.join(valid_data_path, filename))
    if invalid_data:
        json_data["collectionData"] = invalid_data
        create_json(json_data, os.path.join(invalid_data_path, filename))
        print(f"\tInconsistencies found on {collection_name}")
    else:
        print(f"\tNo inconsistencies found on {filename}")

    if error_log:
        create_json(error_log, os.path.join(error_log_path, filename))


def create_json(data, filename):
    if filename[-5:] != ".json":
        filename = "{}.json".format(filename)
    with open(filename, 'w') as fn:
        json.dump(data, fn, indent=2)


def read_config(config_file):
    cnf_file = open(config_file, 'r')
    configuration = json.loads(cnf_file.read())
    return configuration


def read_data(data_path, data_file):
    collection_data = open(os.path.join(data_path, data_file), 'r')
    collection_data = collection_data.read()
    collection_data = json.loads(collection_data)
    return collection_data


def read_schema(schema_path, schema_file, remove_id_pattern=True):
    schema_data = open(os.path.join(schema_path, schema_file), 'r')
    schema_data = schema_data.read()
    schema_data = json.loads(schema_data)
    if remove_id_pattern is True:
        schema_data = remove_id_pattern_from_schema(schema_data)
    return schema_data
