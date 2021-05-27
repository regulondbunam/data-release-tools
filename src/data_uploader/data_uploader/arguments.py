import argparse


def load():
    parser = argparse.ArgumentParser(description="Loads JSON files into the specified database",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="Either [Multigenomic or Datamarts] and [Directory or File] should be selected through arguments options"
                                     )

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        "-i", "--inputdir",
        help="Input JSON data path whose source identifiers will be replaced with RegulonDB's identifiers",
        metavar="/Users/pablo/Proyectos/RegulonDB/Results/replaced_identifiers/multigenomic/ecocyc",
    )

    input_group.add_argument(
        "-f", "--file",
        help="Input JSON data path whose source identifiers will be replaced with RegulonDB's identifiers",
        metavar="/Users/pablo/Proyectos/RegulonDB/Results/replaced_identifiers/multigenomic/ecocyc/gene.json"
    )

    parser.add_argument(
        "-u", "--url",
        help="URL to establish a connection between the process and MongoDB",
        metavar="mongodb://pablo:pablo@127.0.0.1:27017/multigenomic",
        required=True
    )

    db_group = parser.add_mutually_exclusive_group(required=True)

    db_group.add_argument(
        "-mg", "--regulondbmultigenomic",
        action="store_true",
        help="Sets the process for MultiGenomic DB"
    )

    db_group.add_argument(
        "-dm", "--regulondbdatamarts",
        action="store_true",
        help="Sets the process for Datamarts DB"
    )

    parser.add_argument(
        "-l", "--log",
        help="Path where the log of the process will be stored.",
        metavar="/Users/pablo/Proyectos/RegulonDB/Results/log",
        default="/Users/pablo/Proyectos/RegulonDB/Results/log"
    )

    arguments = parser.parse_args()
    return arguments
