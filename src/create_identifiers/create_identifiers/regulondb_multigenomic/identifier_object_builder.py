from .domain.evidence import evidence
from .domain.external_cross_reference import external_cross_reference
from .domain.gene import gene
from .domain.motif import motif
from .domain.ontology import ontology
from .domain.operon import operon
from .domain.product import product
from .domain.promoter import promoter
from .domain.publication import publication
from .domain.regulatory_complex import regulatory_complex
from .domain.regulatory_continuant import regulatory_continuant
from .domain.regulatory_interaction import regulatory_interaction
from .domain.sigma_factor import sigma_factor
from .domain.term import term
from .domain.terminator import terminator
from .domain.transcription_factor import transcription_factor
from .domain.transcription_factor_regulatory_site import transcription_factor_regulatory_site
from .domain.transcription_unit import transcription_unit


def build_identifier_object(object_id, **kwargs):
    identifier = {
        "_id": object_id,
        "classAcronym": kwargs.get("classAcronym", None),
        "createdOnRegulonDBRelease": kwargs.get("regulondbReleaseVersion", None),
        "lastRegulonDBReleaseUsed": kwargs.get("regulondbReleaseVersion", None),
        "objectOriginalSourceId": object_id,
        "ontologyName": kwargs.get("ontologyName", None),
        "organism": kwargs.get("organism", None),
        "propertiesToMakeId": kwargs.get("uniqueDataString", None),
        "regulondbDatabase": kwargs.get("database", None),
        "sourceDBName": kwargs.get("sourceDBName", None),
        "sourceDBVersion": kwargs.get("sourceDBVersion", None),
        "subClassAcronym": kwargs.get("subClassAcronym", None),
        "type": kwargs.get("type", None)
    }

    return identifier


get_unique_data = {
    "evidences": evidence,
    "externalCrossReferences": external_cross_reference,
    "genes": gene,
    "motifs": motif,
    "ontologies": ontology,
    "operons": operon,
    "products": product,
    "promoters": promoter,
    "publications": publication,
    "regulatoryComplexes": regulatory_complex,
    "regulatoryContinuants": regulatory_continuant,
    "regulatoryInteractions": regulatory_interaction,
    "sigmaFactors": sigma_factor,
    "terms": term,
    "terminators": terminator,
    "transcriptionFactors": transcription_factor,
    "regulatorySites": transcription_factor_regulatory_site,
    "transcriptionUnits": transcription_unit,
}


def remove_organism_property_from(identifier_object):
    if identifier_object["type"] in ["ontologies", "term"]:
        identifier_object["organism"] = None


def set_identifier_object(json_object, collection_name,  **metadata_properties):
    # print(collection_name)
    # if collection_name not in ["ontologies", "terms"] else "ontologies"
    if collection_name == "segments":
        return None
    metadata_properties["type"] = collection_name
    metadata_properties["uniqueDataString"] = get_unique_data[collection_name](
        **json_object)

    object_id = json_object["_id"]

    identifier_object = build_identifier_object(
        object_id, **metadata_properties)
    remove_organism_property_from(identifier_object)

    return identifier_object
