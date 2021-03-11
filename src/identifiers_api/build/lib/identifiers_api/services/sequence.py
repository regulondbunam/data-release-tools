from identifiers_api.models.sequences import Sequence
from mongoengine.errors import DoesNotExist


def get_sequence(class_acronym, organism, regulondb_database, subclass_acronym, type_):
    try:
        sequence = Sequence.objects.get(database=regulondb_database, organism=organism, type_=type_)
    except DoesNotExist:
        create_sequence(class_acronym, regulondb_database, organism, subclass_acronym, type_)
        sequence = Sequence.objects.get(database=regulondb_database, organism=organism, type_=type_)
    return sequence


def create_sequence(class_acronym, database, organism, subclass_acronym, type_):
    sequence = Sequence()
    sequence.classAcronym = class_acronym
    sequence.database = database
    sequence.organism = organism
    sequence.subclassAcronym = subclass_acronym
    sequence.type_ = type_
    sequence.value = 1
    sequence.save()


def update_sequence_value(sequence: Sequence):
    sequence.update(value=sequence.value + 1)
    sequence.save()
