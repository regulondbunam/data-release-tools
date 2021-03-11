from pymongo import MongoClient
from datetime import datetime


class Identifiers(object):
    multigenomic_acronyms = {
        "evidence": "EV",
        "externalCrossReference": "ER",
        "gene": "GN",
        "motif": "MT",
        "ontology": "OT",
        "operon": "OP",
        "product": "PD",
        "promoter": "PM",
        "promoterFeature": "PF",
        "publication": "PR",
        "regulatoryComplex": "RC",
        "regulatoryContinuant": "CN",
        "regulatoryInteraction": "RI",
        "sigmaFactor": "SF",
        "term": "TR",
        "terminator": "TM",
        "regulatorySite": "BS",
        "transcriptionUnit": "TU"
    }
    datamart_acronyms = {
        "gene_product": "GP",
        "regulator": "RG"
    }

    def __init__(self, connection_url, regulondb_version=None, is_multigenomic=True, database="multigenomic", organism="ECOLI", identifier_collection="identifier"):
        self.client = MongoClient(connection_url)
        self.db_conn = self.client[database]
        self.identifier_collection = self.db_conn[identifier_collection]
        self.new_identifiers_to_insert = []
        self.organism = organism
        self.regulondb_version = regulondb_version
        self.sequence_collection = self.db_conn["sequence"]
        self.acronyms = self.multigenomic_acronyms if is_multigenomic else self.datamart_acronyms

    def build_identifier_object(self, source_object_data, next_sequence_value):
        identifier = {
            "_id": "RDB{}{}{}".format(self.organism, self.acronyms[source_object_data["type"]], next_sequence_value),
            "creationDate": datetime.utcnow().strftime('%d %B %Y - %H:%M:%S'),
            "history": [
                {
                    "uniqueDataString": source_object_data["unique_data_string"],
                    "sourceData": {
                        "source": source_object_data["source"],
                        "version": source_object_data["source_version"]
                    }
                }
            ],
            "regulonDBVersion": self.regulondb_version,
            "sourceObject_id": source_object_data["id"],
            "type": source_object_data["type"]
        }
        return identifier

    def create_autoincrement_sequence_for(self, entity=None):
        self.sequence_collection.insert({
            'entity': entity,
            'id': 0
        })

    def get_next_sequence_value(self, entity=None, size=1):
        if not self.sequence_collection.find_one({'entity': entity}):
            self.create_autoincrement_sequence_for(entity)
        next_sequence_value = self.sequence_collection.find_one_and_update(
            {'entity': entity},
            {'$inc': {"id": size}},
            new=True
        ).get('id')
        next_sequence_value = str(next_sequence_value)
        next_sequence_value = "0" * \
            (5 - len(next_sequence_value)) + next_sequence_value
        return next_sequence_value

    def get_identifier_of(self, source_id, entity=None):
        '''
        One single search
        :param source_id (str): Source id of the object.
        :param entity (str): The entity type of the object.
        :return response(dict): A one key dictionary. Source_id: RegulonDB_Identifier
        '''
        response = None
        if source_id:
            query = {"sourceObject_id": source_id}
            if entity is not None:
                query['type'] = entity
            response = self.identifier_collection.find_one(
                query, {"_id", "sourceObject_id"})
            if response:
                response = {
                    response["sourceObject_id"]: response["_id"]
                }
        return response

    def get_identifiers_of(self, entity=None):
        if entity == "promoter":
            return self.get_promoter_identifiers()
        elif entity == "regulatoryInteraction":
            return self.get_regulatory_interaction_identifiers()
        else:
            results = []
            if entity is not None:
                query = {"type": entity}
                results = self.identifier_collection.find(query)
            identifiers_mapping = {}
            for result in results:
                identifiers_mapping[result["sourceObject_id"]] = result["_id"]
            return {entity: identifiers_mapping}

    def get_all_multigenomic_identifiers(self):
        results = None
        multigenomic_identifiers = {}
        for entity in self.multigenomic_acronyms.keys():
            identifiers_mapping = {}
            if entity is not None:
                query = {"type": entity}
                results = self.identifier_collection.find(query)
            for result in results:
                identifiers_mapping[result["sourceObject_id"]] = result["_id"]
            multigenomic_identifiers[entity] = identifiers_mapping.copy()
        return multigenomic_identifiers

    def get_promoter_identifiers(self):
        identifiers_mapping = {
            "promoter": self.get_identifiers_of("promoter"),
            "promoterFeature": self.get_identifiers_of("promoterFeature")
        }
        return identifiers_mapping

    def get_regulatory_interaction_identifiers(self):
        identifiers_mapping = {
            "regulatoryInteraction": self.get_identifiers_of("regulatoryInteraction"),
            "regulatorySite": self.get_identifiers_of("regulatorySite")
        }
        return identifiers_mapping

    def insert_identifiers(self):
        if self.new_identifiers_to_insert:
            self.identifier_collection.insert_many(
                self.new_identifiers_to_insert
            )
            self.new_identifiers_to_insert = []

    def create_identifier_for(self, source_object_data=None, entity=None):
        next_sequence_value = self.get_next_sequence_value(entity)
        identifier = self.build_identifier_object(
            source_object_data, next_sequence_value)
        print(identifier)
        self.identifier_collection.insert(
            identifier
        )
        # self.new_identifiers_to_insert.append(identifier.copy())

    def __del__(self):
        self.client.close()
