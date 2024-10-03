def gc(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("_id", "NoId"),
        identifier_properties.get("gcPhrase", "NogcPhrase")
    ]

    return unique_data_string
