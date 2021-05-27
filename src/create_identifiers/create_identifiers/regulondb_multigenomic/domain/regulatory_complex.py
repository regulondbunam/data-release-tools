ACRONYM = "RCC"


def regulatory_complex(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("abbreviatedName", "NoAbbreviatedName"),
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("type", "NoType"),
    ]

    return unique_data_string
