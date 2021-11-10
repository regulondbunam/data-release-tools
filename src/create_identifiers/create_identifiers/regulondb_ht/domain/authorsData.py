def author_data(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("tfBindingAuthorsData", "NoAuthorData"),
    ]

    return unique_data_string
