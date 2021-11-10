def dataset(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("datasetType", "NoDatasetType"),
        identifier_properties.get("temporalID", "NoTempID")
    ]

    return unique_data_string
