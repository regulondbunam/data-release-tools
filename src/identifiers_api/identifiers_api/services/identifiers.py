from datetime import datetime

from identifiers_api.services import sequences
from identifiers_api.models.identifiers import Identifiers
from identifiers_api.shared.acronyms import *


def _set_identifier(identifiers_object, sequence):
    db_acronym = get_db_acronym(identifiers_object)
    class_acronym = identifiers_object["classAcronym"]
    sub_class_acronym = identifiers_object["subClassAcronym"]
    sequence_value = sequence.format_value()

    if "ontologies" == identifiers_object["type"]:
        identifier = "".join([db_acronym, class_acronym, sub_class_acronym, "00001"])
    else:
        identifier = "".join([db_acronym, class_acronym, sub_class_acronym, sequence_value])

    return identifier


def create_identifiers_document(identifiers_object):
    identifier = Identifiers()
    identifier.id = identifiers_object.get("_id", None)
    identifier.creationDate = datetime.utcnow().strftime('%d-%m-%Y - %H:%M:%S')
    identifier.createdOnRegulonDBRelease = identifiers_object.get("createdOnRegulonDBRelease", None)
    identifier.lastRegulonDBReleaseUsed = identifiers_object.get("lastRegulonDBReleaseUsed", None)
    identifier.lastUpdate = datetime.utcnow().strftime('%d-%m-%Y - %H:%M:%S')
    identifier.objectOriginalSourceId = identifiers_object.get("objectOriginalSourceId", None)
    identifier.ontologyName = identifiers_object.get("ontologyName", None)
    identifier.organism = identifiers_object.get("organism", None)
    identifier.propertiesToMakeId = identifiers_object.get("propertiesToMakeId", None)
    identifier.regulondbDatabase = identifiers_object.get("regulondbDatabase", None)
    identifier.sequence_id = identifiers_object.get("sequence_id", None)
    identifier.sourceDBName = identifiers_object.get("sourceDBName", None)
    identifier.sourceDBVersion = identifiers_object.get("sourceDBVersion", None)
    identifier.type = identifiers_object.get("type", None)
    identifier.save(force_insert=True)


def create_id(identifiers_object):

    sequence_associated = sequences.get_sequence(identifiers_object)
    object_id = _set_identifier(identifiers_object, sequence_associated)
    identifiers_object["_id"] = object_id
    identifiers_object["sequence_id"] = sequence_associated.id

    create_identifiers_document(identifiers_object)

    if identifiers_object["type"] != "ontologies":
        sequence_associated.update_sequence_value()


def update_id(object_id, regulondb_version):
    identifier = Identifiers.objects.get(_id=object_id)
    identifier.lastRegulonDBReleaseUsed = regulondb_version
    identifier.lastUpdate = datetime.utcnow().strftime('%d-%m-%Y - %H:%M:%S')
    identifier.save()


def get_identifiers(collection_name, regulondb_database, organism):
    mapping_identifiers = {}

    identifiers = Identifiers.objects(type=collection_name, regulondbDatabase=regulondb_database, organism=organism).only("id").only("objectOriginalSourceId")

    for identifier in identifiers:
        mapping_identifiers[identifier.objectOriginalSourceId] = identifier.id

    return mapping_identifiers
