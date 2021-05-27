ACRONYM = "OPC"


def operon(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("regulationPositions", {}).get("leftEndPosition", "NoLEND"),
        identifier_properties.get("regulationPositions", {}).get("rightEndPosition", "NoREND")
    ]

    return unique_data_string
