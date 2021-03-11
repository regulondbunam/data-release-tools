from mongoengine import fields
from mongoengine import DynamicDocument
from .sequences import Sequences


class Identifiers(DynamicDocument):
    id = fields.StringField(required=False, db_field="_id", primary_key=True)
    creationDate = fields.StringField(required=True)
    createdOnRegulonDBRelease = fields.StringField(required=True)
    regulondbDatabase = fields.StringField(required=True)
    lastRegulonDBReleaseUsed = fields.StringField(required=True)
    lastUpdate = fields.StringField(required=True)
    objectOriginalSourceId = fields.StringField(required=True)
    ontologyName = fields.StringField(required=False)
    organism = fields.StringField(required=False)
    propertiesToMakeId = fields.ListField(required=True)
    sequence_id = fields.LazyReferenceField(Sequences, required=True)
    sourceDBName = fields.StringField(required=True)
    sourceDBVersion = fields.StringField(required=True)
    type = fields.StringField(required=True, db_field="type")
