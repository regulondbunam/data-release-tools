from identifiers_api.models.identifiers import Identifiers
from identifiers_api.shared.constants import *


def _get_all_ontologies_related_ids_from(regulondb_version, regulondb_database):
    multigenomicdb_identifiers = {}
    for collection_name in ["ontologies", "terms"]:
        identifiers = Identifiers.objects(type=collection_name, regulondbDatabase=regulondb_database, lastRegulonDBReleaseUsed=regulondb_version).only("id").only("objectOriginalSourceId")
        collection_identifiers = {}
        for identifier in identifiers:
            collection_identifiers[identifier.objectOriginalSourceId] = identifier.id
        multigenomicdb_identifiers[collection_name] = collection_identifiers.copy()
    return multigenomicdb_identifiers


def _get_identifiers_from(organism, regulondb_version, regulondb_database):
    multigenomicdb_identifiers = {}
    collections_names = list(RDB_MULTIGENOMIC_SUBCLASS_ACRONYMS.keys())
    for collection_name in collections_names:
        collection_identifiers = {}
        identifiers = Identifiers.objects(type=collection_name,
                                          organism=organism,
                                          regulondbDatabase=regulondb_database,
                                          lastRegulonDBReleaseUsed=regulondb_version).only(
            "id").only("objectOriginalSourceId")
        for identifier in identifiers:
            collection_identifiers[
                identifier.objectOriginalSourceId] = identifier.id
        multigenomicdb_identifiers[
            collection_name] = collection_identifiers.copy()
    return multigenomicdb_identifiers


def get_all_identifiers(regulondb_version, organism, regulondb_database="regulondbmultigenomic"):
    multigenomicdb_identifiers = _get_identifiers_from(organism, regulondb_version, regulondb_database)
    multigenomicdb_identifiers.update(_get_all_ontologies_related_ids_from(regulondb_version, regulondb_database))
    return multigenomicdb_identifiers


def get_identifiers_by(type, organism=None, ontology_name=None, regulondb_database="regulondbmultigenomic"):
    collection_identifiers = {}
    if ontology_name is not None:
        identifiers = Identifiers.objects(type=type, ontologyName=ontology_name, regulondbDatabase=regulondb_database).only("id").only("objectOriginalSourceId")
    elif organism is not None:
        identifiers = Identifiers.objects(type=type, organism=organism, regulondbDatabase=regulondb_database).only("id").only("objectOriginalSourceId")
    else:
        identifiers = Identifiers.objects(type=type, regulondbDatabase=regulondb_database).only("id").only("objectOriginalSourceId")
    for identifier in identifiers:
        collection_identifiers[identifier.objectOriginalSourceId] = identifier.id
    return collection_identifiers


def create_id():
    pass