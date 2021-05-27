from datetime import datetime

from identifiers_api.services import sequences
from identifiers_api.models.identifiers import Identifier

from identifiers_api.shared.constants import *

def get_db_acronym(database):
    if database in REGULONDB_DATABASES_ACRONYMS:
        return REGULONDB_DATABASES_ACRONYMS[database]
    return "RDB"


def get_class_acronym(organism, type_):
    if organism and type_ not in ["term", "ontology"]:
        class_acronym = ORGANISM_CLASS_ACRONYMS[organism.lower()]
    else:
        class_acronym = GLOBAL_CLASS_ACRONYMS[type_]
    return class_acronym


def get_subclass_acronym(organism, rdb_database, type_):
    if rdb_database == "regulondbmultigenomic" and type_ not in ["term", "ontology"]:
        subclass_acronym = RDB_MULTIGENOMIC_SUBCLASS_ACRONYMS[type_]
    elif rdb_database == "regulondbmultigenomic" and organism in ONTOLOGY_SUBCLASS_ACRONYMS:
        subclass_acronym = ONTOLOGY_SUBCLASS_ACRONYMS[organism]
    elif rdb_database == "regulondbht":
        subclass_acronym = RDB_HT_SUBCLASS_ACRONYMS[type_]
    else:
        raise ValueError("Subclass could not be determined")
    return subclass_acronym


def get_id_acronym(organism, rdb_database, type_):
    class_acronym = get_class_acronym(organism, type_)
    subclass_acronym = get_subclass_acronym(organism, rdb_database, type_)
    return "".join([class_acronym, subclass_acronym])


def create_identifier_document(identifier_object):
    identifier = Identifier()
    identifier.id = identifier_object.get("_id", None)
    identifier.creationDate = datetime.utcnow().strftime('%d-%m-%Y - %H:%M:%S')
    identifier.createdOnRegulonDBRelease = identifier_object.get("createdOnRegulonDBRelease", None)
    identifier.lastRegulonDBReleaseUsed = identifier_object.get("lastRegulonDBReleaseUsed", None)
    identifier.lastUpdate = datetime.utcnow().strftime('%d-%m-%Y - %H:%M:%S')
    identifier.objectOriginalSourceId = identifier_object.get("objectOriginalSourceId", None)
    identifier.organism = identifier_object.get("organism", None)
    identifier.propertiesToMakeId = identifier_object.get("propertiesToMakeId", None)
    identifier.regulondbDatabase = identifier_object.get("regulondbDatabase", None)
    identifier.sequence_id = identifier_object.get("sequence_id", None)
    identifier.sourceName = identifier_object.get("sourceName", None)
    identifier.sourceVersion = identifier_object.get("sourceVersion", None)
    identifier.type_ = identifier_object.get("type", None)
    identifier.save(force_insert=True)


def create_id(identifier_object):
    database = identifier_object.get("regulondbDatabase", None)
    organism = identifier_object.get("organism", None)
    type_ = identifier_object.get("type", None)

    db_acronym = get_db_acronym(database)
    class_acronym = get_class_acronym(organism, type_)
    subclass_acronym = get_subclass_acronym(organism, database, type_) if class_acronym != "ONTOLOGY" else ""

    sequence_associated = sequences.get_sequence(class_acronym, organism, database, subclass_acronym, type_)

    object_id = "".join([db_acronym, class_acronym, subclass_acronym, sequence_associated.format_value()])
    identifier_object["_id"] = object_id
    identifier_object["sequence_id"] = sequence_associated.id

    create_identifier_document(identifier_object)

    sequence_associated.update_sequence_value()


def update_id(object_id, regulondb_version):
    identifier = Identifier.objects.get(_id=object_id)
    identifier.lastRegulonDBReleaseUsed = regulondb_version
    identifier.lastUpdate = datetime.utcnow().strftime('%d-%m-%Y - %H:%M:%S')
    identifier.save()


def get_identifiers(collection_name, regulondb_database, organism):
    mapping_identifiers = {}

    identifiers = Identifier.objects(type=collection_name, regulondbDatabase=regulondb_database, organism=organism).only("id").only("objectOriginalSourceId")

    for identifier in identifiers:
        mapping_identifiers[identifier.objectOriginalSourceId] = identifier.id

    return mapping_identifiers