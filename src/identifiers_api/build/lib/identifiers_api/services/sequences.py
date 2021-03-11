from identifiers_api.models.sequences import Sequences
from mongoengine.errors import DoesNotExist


def _get_sequence(identifiers_object):
    regulondb_database = identifiers_object["regulondbDatabase"]
    ontology_name = identifiers_object.get("ontologyName", None)
    organism = identifiers_object.get("organism", None)
    type_ = identifiers_object["type"]
    if ontology_name:
        sequence = Sequences.objects.get(database=regulondb_database,
                                         ontologyName=ontology_name)
    else:
        sequence = Sequences.objects.get(database=regulondb_database,
                                         organism=organism, type=type_)
    return sequence


def get_sequence(identifiers_object):
    try:
        sequence = _get_sequence(identifiers_object)
    except DoesNotExist:
        create_sequence(identifiers_object)
        sequence = _get_sequence(identifiers_object)
    return sequence


def create_sequence(identifiers_object):
    sequence = Sequences()
    sequence.classAcronym = identifiers_object["classAcronym"]
    sequence.database = identifiers_object["regulondbDatabase"]
    sequence.ontologyName = identifiers_object.get("ontologyName", None)
    sequence.organism = identifiers_object.get("organism", None)
    sequence.subclassAcronym = identifiers_object["subClassAcronym"]
    sequence.type = "ontologies" if identifiers_object["type"] in ["ontologies", "terms"] else identifiers_object["type"]
    sequence.value = 2 if identifiers_object["type"] in ["ontologies", "terms"] else 1
    sequence.save()


def update_sequences_value(sequence: Sequences):
    sequence.update(value=sequence.value + 1)
    sequence.save()
