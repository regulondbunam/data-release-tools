ACRONYM = "RIC"


def regulatory_interaction(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("function", "NoFunction"),
        identifier_properties.get("name", "NoNameRegulatedEntity"),
        identifier_properties.get("regulator", "NoRegulator")
    ]

    return unique_data_string
