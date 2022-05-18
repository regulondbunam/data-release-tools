def gex(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("dataset_ids", "NoDatasetIds"),
    ]

    return unique_data_string
