import utils
import arguments
'''

## Usage
```
python2 data_validator.py
```

'''


def run(paths, remove_id_pattern=True):
    utils.verify_paths(paths)
    # Loading schemas and removing "pattern" property value if
    # remove_id_pattern is true. Due to how the identifiers are created
    # on RegulonDB, we need to first validate the data before assigning them
    # persisting identifiers
    schemas = utils.load_schemas(
        paths["schema_path"], remove_id_pattern=remove_id_pattern)
    jsons_data = utils.load_jsons(paths["data_path"])
    for filename, json_data in jsons_data.items():
        try:
            print(f"Validating data from: {filename}")
            collection_name = json_data["collectionName"]
            utils.validate_data(schemas[collection_name], filename, json_data,
                                paths["valid_path"], paths["invalid_path"], paths["log_path"])
        except KeyError:
            print(
                f"There's no schema rules for {collection_name} data. Moving all the data as valid.")


if __name__ == '__main__':

    args = arguments.load_arguments()

    remove_id_pattern = args.skippattern

    paths = {
        "data_path": args.inputdir,
        "schema_path": args.schemas,
        "log_path": args.log,
        "valid_path": args.validoutputdir,
        "invalid_path": args.invalidoutputdir
    }
    run(paths, remove_id_pattern)
    print("Results on:")
    print(f'\t {paths["valid_path"]} for valid data')
    print(f'\t {paths["invalid_path"]} for invalid data')
    print(
        f'\t {paths["log_path"]} for more information about the invalid data')
