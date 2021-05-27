import argparse


def load_arguments():
    parser = argparse.ArgumentParser(description="JSON Data Validator", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "-i", "--inputdir",
        help="Input JSON path data whose information will be validated it",
        metavar="/Users/RegulonDB/Results/source/ecocyc",
    )
    parser.add_argument(
        "-s", "--schemas",
        help="Directory that contains the schemas that will be used to validate the input data",
        metavar="/Users/RegulonDB/Results/schemas/multigenomic"
    )
    parser.add_argument(
        "-sp", "--skippattern",
        help="If set, then removes the id pattern from the schema. Recommend it when the data has the source ids and not RegulonDB ids",
        action='store_true'
    )
    parser.add_argument(
        "-v", "--validoutputdir",
        help="Directory that will contain all the valid data",
        metavar="/Users/RegulonDB/Results/valid_data/ecocyc"
    ),
    parser.add_argument(
        "-iv", "--invalidoutputdir",
        help="Directory that will contain all the invalid(not valid) data",
        metavar="/Users/RegulonDB/Results/invalid_data/ecocyc"
    )
    parser.add_argument(
        "-l", "--log",
        help="Directory that contains log of the invalid data, the reason why the data is being rejected.",
        metavar="/Users/RegulonDB/Results/log/data_validator"
    )

    arguments = parser.parse_args()

    return arguments
