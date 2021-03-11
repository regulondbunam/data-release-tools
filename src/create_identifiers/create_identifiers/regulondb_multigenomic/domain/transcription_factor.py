ACRONYM = "TFC"


def transcription_factor(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("activeConformations", "NoActiveConformations"),
        identifier_properties.get("globalFunction", "NoGlobalFunction")
    ]

    return unique_data_string
