
def build_identifier_object(object_source_id, uniqueDataString, source, source_version, organism, regulondb_version, regulondb_database, type_):
    identifier_object = {
        "_id": object_source_id,
        "createdOnRegulonDBRelease": regulondb_version,
        "lastRegulonDBReleaseUsed": regulondb_version,
        "objectOriginalSourceId": object_source_id,
        "organism": organism,
        "propertiesToMakeId": uniqueDataString,
        "regulondbDatabase": regulondb_database,
        "sourceName": source,
        "sourceVersion": source_version,
        "type": type_
    }
    return identifier_object


def evidence(entity_data, source, source_version, organism, regulondb_version, regulondb_database):
    unique_data_string = [
        entity_data.get("name", "NoName"),
        entity_data.get("code", "NoCode")
    ]
    yield build_identifier_object(entity_data["_id"], unique_data_string, source, source_version, organism, regulondb_version, regulondb_database, "evidence")



entity_data = {}
entity_data["_id"] = "hola"
entity_data["name"] = "pruebaname"
entity_data["code"] = "pruebacode"
new_evidence = evidence(entity_data, "ecocyc", "24.5", "ecoli", "10.6", "regulondbmultigenomic")
print(new_evidence)