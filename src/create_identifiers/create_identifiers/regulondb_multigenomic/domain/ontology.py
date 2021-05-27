ACRONYM = "ONTOL"


def ontology(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName")
    ]

    return unique_data_string
