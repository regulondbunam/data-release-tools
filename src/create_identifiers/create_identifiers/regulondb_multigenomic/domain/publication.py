ACRONYM = "PRC"


def publication(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("pmid", "NoPMID"),
        identifier_properties.get("title", "NoTitle"),
        identifier_properties.get("year", "NoYear"),
    ]
    return unique_data_string
