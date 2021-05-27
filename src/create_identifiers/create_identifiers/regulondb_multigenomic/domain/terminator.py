ACRONYM = "TMC"


def terminator(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("class", "NoClass"),
        identifier_properties.get("transcriptionTerminationSite", {}).get("leftEndPosition", "NoTTSLEND"),
        identifier_properties.get("transcriptionTerminationSite", {}).get("rightEndPosition", "NoTTSREND")
    ]

    return unique_data_string
