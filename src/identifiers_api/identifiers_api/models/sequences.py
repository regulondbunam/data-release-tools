from mongoengine import fields
from mongoengine import Document


class Sequences(Document):
    classAcronym = fields.StringField(required=True)
    database = fields.StringField(required=True)
    ontologyName = fields.StringField(required=False)
    organism = fields.StringField(required=False)
    subclassAcronym = fields.StringField(required=True)
    type = fields.StringField(required=True, db_field="type")
    value = fields.IntField(required=True)

    def format_value(self):
        return "0" * (5 - len(str(self.value))) + str(self.value)

    def update_sequence_value(self):
        self.update(value=self.value + 1)
        self.save()