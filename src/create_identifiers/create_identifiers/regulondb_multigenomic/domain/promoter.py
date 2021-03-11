ACRONYM = "PMC"


def promoter(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("pos1", "NoPos1"),
        identifier_properties.get("transcriptionStartSite", {}).get("leftEndPosition", "NoTSSLEND"),
        identifier_properties.get("transcriptionStartSite", {}).get("rightEndPosition", "NoTSSREND")
    ]

    return unique_data_string
