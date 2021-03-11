ACRONYM = "BSC"


def transcription_factor_regulatory_site(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("absolutePosition", "NoAbsolutePosition"),
        identifier_properties.get("leftEndPosition", "NoLEND"),
        identifier_properties.get("rightEndPosition", "NoREND")
    ]

    return unique_data_string
