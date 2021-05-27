from mongoengine import fields
from mongoengine import DynamicDocument
from .sequence import Sequence


class Identifier(DynamicDocument):
    id = fields.StringField(required=False, db_field="_id", primary_key=True)
    creationDate = fields.StringField(required=True)
    createdOnRegulonDBRelease = fields.StringField(required=True)
    regulondbDatabase = fields.StringField(required=True)
    lastRegulonDBReleaseUsed = fields.StringField(required=True)
    lastUpdate = fields.StringField(required=True)
    objectOriginalSourceId = fields.StringField(required=True)
    organism = fields.StringField(required=True)
    propertiesToMakeId = fields.ListField(required=True)
    sequence_id = fields.LazyReferenceField(Sequence, required=True)
    sourceName = fields.StringField(required=True)
    sourceVersion = fields.StringField(required=True)
    type_ = fields.StringField(required=True, db_field="type")
