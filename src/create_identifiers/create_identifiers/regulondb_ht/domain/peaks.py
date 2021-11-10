def peaks(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("peakLeftPosition", "NoLEND"),
        identifier_properties.get("peakRightPosition", "NoREND"),
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("score", "NoScore"),
    ]

    return unique_data_string
