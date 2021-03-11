ACRONYM = "TUC"


def transcription_unit(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("operon_id", "NoOperon")
    ]

    return unique_data_string
