from identifiers_api.models.identifiers import Identifier
from identifiers_api.services import sequences

REGULONDB_DATABASES_ACRONYMS = {
    "regulondbmultigenomic": "RDB",
    "regulondbht": "RHT"
}

RDB_MULTIGENOMIC_SUBCLASS_ACRONYMS = {
    "evidence": "EVC",
    "externalCrossReference": "ERC",
    "gene": "GNC",
    "motif": "MTC",
    "operon": "OPC",
    "product": "PDC",
    "promoter": "PMC",
    "promoterFeature": "PFC",
    "publication": "PRC",
    "regulatoryComplex": "RCC",
    "regulatoryContinuant": "CNC",
    "regulatoryInteraction": "RIC",
    "sigmaFactor": "SFC",
    "transcriptionFactorRegulatorySite": "STC",
    "terminator": "TMC",
    "transcriptionFactorRegulatorySite": "BSC",
    "transcriptionUnit": "TUC"
}

ORGANISM_CLASS_ACRONYMS = {
    "ecoli": "ECOLI"
}

GLOBAL_CLASS_ACRONYMS = {
    "metadata": "METADATA",
    "ontology": "ONTOL"
}


RDB_HT_SUBCLASS_ACRONYMS = {
    "geneExpressions": "GED",
    "tfBindings": "BSD",
    "transcriptionStartSites": "SSD",
    "transcriptionTerminatorSites": "TSD",
    "transcriptionUnits": "TUD",
    "regulatoryInteractions": "RID",
    "geneExpressionContrasts": "GEC",
    "tfBindingContrasts": "BSC",
    "transcriptionStartSiteContrasts": "SSC",
    "transcriptionTerminatorSiteContrasts": "TSC",
    "transcriptionUnitContrasts": "TUC",
    "regulatoryInteractionContrasts": "RIC",
    "contrasts": "CON",
    "samples": "SAM",
    "series": "SRS",
    "platforms": "PTF"
}


ONTOLOGY_SUBCLASS_ACRONYMS = {
    "geneOntology": "GON",
    "multifun": "MTF",
    "microbialConditionOntology": "MCO",
    "prokaryoticRegulationOntology": "PRO",
    "growthConditionPhrasesCatalog": "GCP",
    "growthConditionContrast": "GCC"
}


#TODO: Ver con Gabo y Edgar
DATAMARTS_ACRONYMS = {
    "overviews": ""
}


def get_all(regulondb_type: str, database: str, organism):
    return Identifier.objects(database=database, type=regulondb_type, organism=organism)


def find_one_by_id(database: str, regulondb_type: str, source_id: str, organism: str):
    return Identifier.objects.get(database=database, source_id=source_id, type=regulondb_type, organism=organism)


def set_identifier_object():
    pass


def get_db_acronym(database):
    if database in REGULONDB_DATABASES_ACRONYMS:
        return REGULONDB_DATABASES_ACRONYMS[database]
    return "RDB"


def get_class_acronym(organism, type_):
    if organism and type_ not in ["term", "ontology"]:
        class_acronym = ORGANISM_CLASS_ACRONYMS[organism.lower()]
    else:
        if type_ == "term":
            type_ = "ontology"
        class_acronym = GLOBAL_CLASS_ACRONYMS[type_]
    return class_acronym


def get_subclass_acronym(organism, rdb_database, type_):
    if rdb_database == "regulondbmultigenomic" and type_ != "term":
        subclass_acronym = RDB_MULTIGENOMIC_SUBCLASS_ACRONYMS[type_]
    elif rdb_database == "regulondbmultigenomic" and organism in ONTOLOGY_SUBCLASS_ACRONYMS:
        subclass_acronym = ONTOLOGY_SUBCLASS_ACRONYMS[organism]
    elif rdb_database == "regulondbht":
        subclass_acronym = RDB_HT_SUBCLASS_ACRONYMS[type_]
    else:
        print(organism, rdb_database, type_)
        raise ValueError("Subclass could not be determined")
    return subclass_acronym


def get_id_acronym(organism, rdb_database, type_):
    class_acronym = get_class_acronym(organism, type_)
    subclass_acronym = get_subclass_acronym(organism, rdb_database, type_)
    return "".join([class_acronym, subclass_acronym])


def create_id(identifier_object):
    database = identifier_object.get("regulondbDatabase", None)
    organism = identifier_object.get("organism", None)
    type_ = identifier_object.get("type", None)
    db_acronym = get_db_acronym(database)
    class_acronym = get_class_acronym(organism, type_)
    subclass_acronym = get_subclass_acronym(organism, database, type_)
    identifier = "".join([db_acronym, class_acronym, subclass_acronym])
    sequence_value = sequences.get_sequence_next_value(class_acronym, organism, database, subclass_acronym, type_)
    print("".join([identifier, f"{sequence_value}"]))


def create_ids(database: str, regulondb_type: str, regulondb_version, identifier_object: [dict]):
    pass