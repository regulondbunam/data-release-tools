ACRONYM = "EVC"


def evidence(**identifier_properties):
    unique_data_string = [
        identifier_properties.get("name", "NoName"),
        identifier_properties.get("code", "NoCode")
    ]

    return unique_data_string



if __name__ == '__main__':
    identifier_properties = {
        "entity_data": {
            "name": "name",
            "code": "code"
        }
    }
    print(evidence(**identifier_properties))
