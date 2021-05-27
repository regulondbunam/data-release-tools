import argparse


def load_arguments():
    parser = argparse.ArgumentParser(description="Replaces the data's source identifiers with RegulonDB's identifiers.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="Either Multigenomic or Datamarts or HT should be selected through arguments options"
                                     )

    parser.add_argument(
        "-u", "--url",
        help="URL to establish a connection between the process and MongoDB",
        metavar="mongodb://user:pass@127.0.0.1:27017/regulondbmultigenomic",
        required=False
    )

    parser.add_argument(
        "-i", "--inputdir",
        help="Input JSON path data whose information will be validated it",
        metavar="/Users/user/Proyectos/RegulonDB/Results/source/ecocyc",
        required=True
    )

    parser.add_argument(
        "-org", "--organism",
        help="Input JSON path data whose information will be validated it",
        metavar="/Users/user/Proyectos/RegulonDB/Results/source/ecocyc",
        required=False
    )

    parser.add_argument(
        "-v", "--version",
        help="RegulonDB's release version",
        metavar="10.8",
        required=True
    )

    parser.add_argument(
        "-s", "--source",
        help="Source's name",
        metavar="EcoCyc",
        required=True
    )

    parser.add_argument(
        "-sv", "--sourceversion",
        help="Source's release version",
        metavar="24.0",
        required=True
    )

    parser.add_argument(
        "-l", "--log",
        help="Path where the log is going to be saved.",
        metavar="/Users/user/Proyectos/RegulonDB/Results/log",
        required=True
    )

    parser.add_argument(
        "-db", "--database",
        help="Database that belongs to the objects whose identifiers are going to be created",
        choices=["regulondbmultigenomic", "regulondbht", "regulondbdatamarts"],
        metavar="regulondbmultigenomic"
    )

    arguments = parser.parse_args()

    return arguments
