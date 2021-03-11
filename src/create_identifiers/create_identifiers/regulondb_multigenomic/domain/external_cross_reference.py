ACRONYM = "ERC"


def external_cross_reference(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("url", "NoURL"),
    ]

    return unique_data_string