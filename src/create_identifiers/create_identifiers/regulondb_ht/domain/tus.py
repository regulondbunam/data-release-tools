def tus(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("leftEndPosition", "NoLEND"),
        identifier_properties.get("lightEndPosition", "NoREND"),
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("strand", "NoStrand"),
    ]

    return unique_data_string
