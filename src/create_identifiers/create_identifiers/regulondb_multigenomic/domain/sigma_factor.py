ACRONYM = "SFC"


def sigma_factor(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("gene_id", "NoGeneId"),
    ]

    return unique_data_string
