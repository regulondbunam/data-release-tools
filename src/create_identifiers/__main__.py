import os

import identifiers_api

from create_identifiers.lib import utils
from create_identifiers.lib import arguments

from create_identifiers.regulondb_multigenomic import multigenomic_identifiers


def run(input_path, **kwargs):
    """

    :param paths:
    :param kwargs:
    :return:
    """
    utils.verify_paths(input_path)
    jsons_data = utils.load_files(input_path)
    database = kwargs.get("database", None)

    if database == "regulondbmultigenomic":
        multigenomic_identifiers.manage_ids(jsons_data, **kwargs)
    elif database == "regulondbht":
        pass
    elif database == "regulondbdatamarts":
        pass
    else:
        raise KeyError("Process of creating identifiers for the selected "
                       f"database({database}) has not been implemented or "
                       f"there's a typo, please verify it before continuing")


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

