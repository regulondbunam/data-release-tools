ACRONYM = "CNC"


def regulatory_continuant(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("type", "NoType"),
    ]

    return unique_data_string
