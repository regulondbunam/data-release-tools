import argparse


def load_arguments():
    parser = argparse.ArgumentParser(description="Replaces the data's source identifiers with RegulonDB's identifiers.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="Either Multigenomic or Datamarts should be selected through arguments options"
                                     )
    parser.add_argument(
        "-org", "--organism",
        help="organism name corresponding to the input data",
        metavar="ECOLI",
        required=True
    )


    parser.add_argument(
        "-i", "--inputdir",
        help="Input JSON data path whose source identifiers will be replaced with RegulonDB's identifiers",
        metavar="/Users/user/Proyectos/RegulonDB/Results/source/ecocyc",
        required=True
    )

    parser.add_argument(
        "-o", "--outputdir",
        help="Directory where the JSON files with the RegulonDB IDs replaced will be stored",
        metavar="/Users/user/Proyectos/RegulonDB/Results/replaced_identifiers/multigenomic/ecocyc",
        required=True
    )


    parser.add_argument(
        "-u", "--url",
        help="URL to establish a connection between the process and MongoDB",
        metavar="mongodb://127.0.0.1:27017/regulondbidentifiers",
        required=True
    )

    parser.add_argument(
        "-l", "--log",
        help="Path where the log is going to be saved.",
        metavar="/Users/user/Proyectos/RegulonDB/Results/log",
    )

    parser.add_argument(
        "-db", "--database",
        choices=["regulondbmultigenomic", "regulondbht", "regulondbdatamarts"],
        help="database where the input data belongs",
        metavar="regulondbmultigenomic",
        required=True
    )

    parser.add_argument(
        "-v", "--version",
        help="RegulonDB's release version",
        metavar="10.8",
        required=True
    )

    arguments = parser.parse_args()
    return arguments