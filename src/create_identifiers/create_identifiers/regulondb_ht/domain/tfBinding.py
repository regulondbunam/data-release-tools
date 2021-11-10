from typing import Sequence


def tfBinding(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("chrLeftPosition", "NoLEND"),
        identifier_properties.get("chrRightPosition", "NoREND"),
        identifier_properties.get("score", "NoScore"),
        identifier_properties.get("strand", "NoStrand"),
        identifier_properties.get("sequence", "NoSequence")
    ]

    return unique_data_string
