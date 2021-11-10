from .domain.dataset import dataset
from .domain.authorsData import author_data
from .domain.peaks import peaks
from .domain.tfBinding import tfBinding


def build_identifier_object(object_id, **kwargs):
    identifier = {
        "_id": object_id,
        "childClassAcronym": kwargs.get("childClassAcronym", None),
        "classAcronym": kwargs.get("classAcronym", None),
        "createdOnRegulonDBRelease": kwargs.get("regulondbReleaseVersion", None),
        "lastRegulonDBReleaseUsed": kwargs.get("regulondbReleaseVersion", None),
        "objectOriginalSourceId": object_id,
        "ontologyName": kwargs.get("ontologyName", None),
        "organism": kwargs.get("organism", None),
        "propertiesToMakeId": kwargs.get("uniqueDataString", None),
        "regulondbDatabase": kwargs.get("database", None),
        "sourceDBName": kwargs.get("sourceDBName", None),
        "sourceDBVersion": kwargs.get("sourceDBVersion", None),
        "subClassAcronym": kwargs.get("subClassAcronym", None),
        "type": kwargs.get("type", None)
    }

    return identifier


get_unique_data = {
    "dataset": dataset,
    "peaks": peaks,
    "tfBinding": tfBinding,
    "authorsData": author_data,
}


def set_identifier_object(json_object, collection_name, **metadata_properties):
    # print(collection_name)
    if collection_name == "segments":
        return None
    metadata_properties["type"] = collection_name
    metadata_properties["uniqueDataString"] = get_unique_data[collection_name](
        **json_object)

    object_id = json_object["_id"]

    identifier_object = build_identifier_object(
        object_id, **metadata_properties)

    return identifier_object
