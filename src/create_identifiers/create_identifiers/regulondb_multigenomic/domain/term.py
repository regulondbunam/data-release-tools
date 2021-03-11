ACRONYM = "TRC"


def term(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("label", "NoLabel"),
        identifier_properties.get("oboId", "NoOboId")
    ]

    return unique_data_string