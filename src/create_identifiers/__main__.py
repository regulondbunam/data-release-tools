import os
import json

import identifiers_api

from create_identifiers.lib import utils
from create_identifiers.lib import arguments

from create_identifiers.regulondb_multigenomic import multigenomic_identifiers
from create_identifiers.regulondb_ht import ht_identifiers
from create_identifiers.regulondb_datamarts import datamarts_identifiers


def run(input_path, **kwargs):
    """

    :param paths:
    :param kwargs:
    :return:
    """
    utils.verify_paths(input_path)
    # jsons_data = utils.load_files(input_path)
    print(f"Creating identifiers...")
    database = kwargs.get("database", None)
    print(f"Preparing IDs generations for {database} collections...")
    for filename in os.listdir(input_path):
        if os.path.isdir(os.path.join(input_path, filename)):
            continue
        with open(os.path.join(input_path, filename), 'r') as fp:
            try:
                json_data = json.loads(fp.read())
            except ValueError as value_error:
                print(f"{filename} is not a valid json file. File is being ignored.")
                continue
        if database == "regulondbmultigenomic":
            multigenomic_identifiers.manage_ids(json_data, **kwargs)
        elif database == "regulondbht":
            ht_identifiers.manage_ids(json_data, **kwargs)
        elif database == "regulondbdatamarts":
            datamarts_identifiers.manage_ids(json_data, **kwargs)
        else:
            raise KeyError("Process of creating identifiers for the selected "
                           f"database({database}) has not been implemented or "
                           f"there's a typo, please verify it before continuing")
    print(f"\nSuccessfully created {database} identifiers.")


if __name__ == "__main__":
    arguments = arguments.load_arguments()

    input_data_directory = arguments.inputdir

    regulondb_release_version = os.getenv("RELEASE_VERSION") if os.getenv("RELEASE_VERSION") else arguments.version

    identifiers_api.connect(arguments.url)

    kwargs = {
        "database": arguments.database,
        "regulondbReleaseVersion": regulondb_release_version,
        "sourceDBVersion": arguments.sourceversion,
        "sourceDBName": arguments.source,
        "organism": arguments.organism
    }

    utils.set_log(arguments.log)

    run(input_data_directory, **kwargs)
