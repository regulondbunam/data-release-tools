import json
import os
import jsonschema


def remove_id_pattern_from_schema(schema):
    schema = delete_keys_from_dict(schema, ["pattern"], "^RDB[A-Z]{8}[0-9]{5}$")
    return schema


def delete_keys_from_dict(dictionary_to_update, keys_to_remove, value):
    """
    Delete the keys presented in the keys_to_remove from the dictionary_to_update.
    Loops recursively over nested dictionaries.
    """
    if type(keys_to_remove) is not set:
        keys_to_remove = set(keys_to_remove)
    for k, v in dictionary_to_update.items():
        if k in keys_to_remove:
            if dictionary_to_update[k] == value:
                del dictionary_to_update[k]
        if isinstance(v, dict):
            delete_keys_from_dict(v, keys_to_remove, value)
    return dictionary_to_update


def verify_paths(data_path):
    for path_name, path in data_path.items():
        if not os.path.exists(path):
            raise IOError("Please, verify '{}' directory path".format(path_name))


def _load_files(file_path):
    for filename in os.listdir(file_path):
        if os.path.isdir(os.path.join(file_path, filename)):
            continue
        with open(os.path.join(file_path, filename), 'r') as fp:
            try:
                json_data = json.loads(fp.read())
            except ValueError as value_error:
                print "{} is not a valid json file. File is being ignored.".format(filename)
                continue
        yield filename, json_data


def load_schemas(file_path, remove_id_pattern):
    files = {}
    json_schemas = _load_files(file_path)
    for filename, json_schema in json_schemas:
        if remove_id_pattern is True:
            json_schema = remove_id_pattern_from_schema(json_schema)
        for collection_name, values in json_schema.items():
            files[collection_name] = values
    return files


def load_jsons(file_path):
    files = {}
    jsons_files = _load_files(file_path)
    for filename, json_data in jsons_files:
        files[filename] = json_data
    return files


#TODO: Implementar logica para atrapar todos los errores de un json
def validate_data(collection_schema, filename, json_data, valid_data_path, invalid_data_path, error_log_path):
    valid_data = []
    invalid_data = []
    error_log = []
    collection_data = json_data["collectionData"]
    collection_name = json_data["collectionName"]
    for current_object in collection_data:
        try:
            jsonschema.validate(instance=current_object, schema=collection_schema["validator"]["$jsonSchema"],
                                   format_checker=jsonschema.draft4_format_checker)
            valid_data.append(current_object.copy())
        except jsonschema.exceptions.ValidationError as validation_error:
            invalid_data.append(current_object.copy())
            error_log.append([current_object["_id"], validation_error.message, [element for element in validation_error.path]])

    if valid_data:
        json_data["collectionData"] = valid_data
        create_json(json_data, os.path.join(valid_data_path, filename))
    if invalid_data:
        json_data["collectionData"] = invalid_data
        create_json(json_data, os.path.join(invalid_data_path, filename))
        print "\tInconsistencies found on {}".format(collection_name)
    else:
        print "\tNo inconsistencies found on {}".format(filename)

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
