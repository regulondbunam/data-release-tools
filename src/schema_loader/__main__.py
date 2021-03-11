import argparse
import utils


def load_arguments():
    parser = argparse.ArgumentParser(
        description="Schema loader",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-u", "--url",
        help="MongoDB URL to enable the connection to the database",
        metavar="mongodb://pablo:pablo@127.0.0.1:27017/multigenomic",
        default="mongodb://pablo:pablo@127.0.0.1:27017/multigenomic",
        required=True
    )

    parser.add_argument(
        "-db", "--database",
        help="Name of the database where the schemas are going to be uploaded",
        metavar="multigenomic",
        default="multigenomic",
        required=True
    )

    parser.add_argument(
        "-s", "--schemas",
        help="Directory that contains the schemas that will be loaded",
        metavar="users/pablo-epl/MultigenomicModel/results/json_schema_validation",
        required=True
    )

    parser.add_argument(
        "-d", "--drop",
        help="If the collection already exists, then it will rewrite it (delete and create again).",
        action="store_true"
    )

    parser.add_argument(
        "-fi", "--forcedidentifiers",
        help="If the identifiers collection already exists, then it will rewrite it (delete and create again).",
        action="store_true"
    )

    parser.add_argument(
        "-l", "--log",
        help="Directory that contains log of the invalid data, the reason why the data is being rejected.",
        metavar="/Users/regulondb/"
    )

    arguments = parser.parse_args()

    return arguments


if __name__ == "__main__":
    arguments = load_arguments()
    mongodb_url = arguments.url
    schemas_path = arguments.schemas
    database = arguments.database
    drop = arguments.drop
    forced_identifier = arguments.forcedidentifiers

    db_conn, client = utils.mongodb_connection(mongodb_url, database)

    schemas = utils.load_schemas(schemas_path)

    for collection_name, schema_rules in schemas:
        print("Working on {}".format(collection_name))
        validation_rules = utils.set_collection_schema_rules(collection_name, schema_rules)
        if collection_name not in db_conn.list_collection_names() or (collection_name in db_conn.list_collection_names() and drop is True):
            if collection_name == "identifiers" and forced_identifier is False:
                print("\tCollection {} already exists. Since this is a critical collection you must use both -f and -fi arguments to rewrite it.".format(collection_name))
            else:
                db_conn.drop_collection(collection_name)
                db_conn.create_collection(collection_name)
                db_conn.command(validation_rules)
                print("\t {} created.".format(collection_name))
        else:
            print("Collection {} already exists. If you want to force the creation/recreation of the collection use -f argument".format(collection_name))
    else:
        print("Process executed correctly correctly")
    client.close()

