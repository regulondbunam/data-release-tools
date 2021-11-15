def replace_citations_ids(json_object, identifiers):
    citations = json_object.get("citations", [])
    mapped_evidence_ids = identifiers["evidences"]
    mapped_publication_ids = identifiers["publications"]
    for citation in citations:
        source_evidence_id = citation.get("evidences_id", None)
        source_publication_id = citation.get("publications_id", None)
        if source_evidence_id:
            citation["evidences_id"] = mapped_evidence_ids[source_evidence_id]
        if source_publication_id:
            citation["publications_id"] = mapped_publication_ids[source_publication_id]


def replace_external_cross_references_ids(json_object, identifiers):
    external_cross_references = json_object.get("externalCrossReferences", [])
    mapped_external_cross_reference_ids = identifiers["externalCrossReferences"]
    for external_cross_reference in external_cross_references:
        source_external_cross_reference_id = external_cross_reference["externalCrossReferences_id"]
        external_cross_reference["externalCrossReferences_id"] = mapped_external_cross_reference_ids[source_external_cross_reference_id]


def replace_object_main_id(json_object, identifiers, collection_name):
    mapped_collection_ids = identifiers[collection_name]
    source_object_id = json_object["_id"]
    json_object["_id"] = mapped_collection_ids[source_object_id]


def replace_organism_id(json_object):
    source_organism_id = json_object.get("organisms_id", None)
    if source_organism_id is not None:
        source_organism_id = source_organism_id.upper()
        json_object["organisms_id"] = "RDB{}ORC00001".format(
            source_organism_id)


def evidence(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing organism_id
    replace_organism_id(json_object)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)


def external_cross_references(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing organism_id
    replace_organism_id(json_object)


def gene(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing term_ids
    mapped_term_ids = identifiers["terms"]
    for terms in json_object.get("terms", []):
        source_term_id = terms["terms_id"]
        terms["terms_id"] = mapped_term_ids[source_term_id]
        for parent_terms in terms.get("parents", []):
            source_parent_term_id = parent_terms["terms_id"]
            parent_terms["terms_id"] = mapped_term_ids[source_parent_term_id]

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing organism_id
    replace_organism_id(json_object)


def motif(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing product_ids
    mapped_product_ids = identifiers["products"]
    source_product_id = json_object["products_id"]
    json_object["products_id"] = mapped_product_ids[source_product_id]

    # replacing organism_id
    replace_organism_id(json_object)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)


def ontology(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing organism_id
    replace_organism_id(json_object)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)


def operon(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing gene_ids
    mapped_gene_ids = identifiers["genes"]
    genes = json_object.get("genes", [])
    for gene in genes:
        source_gene_id = gene["genes_id"]
        gene["genes_id"] = mapped_gene_ids[source_gene_id]

    # replacing organism_id
    replace_organism_id(json_object)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)


def product(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing gene_id
    mapped_gene_ids = identifiers["genes"]
    source_gene_id = json_object["genes_id"]
    json_object["genes_id"] = mapped_gene_ids[source_gene_id]

    # replacing term_ids and terms citations_ids
    mapped_term_ids = identifiers["terms"]
    product_terms = json_object.get("terms", {})
    for term_component in product_terms.get("biologicalProcess", []):
        source_term_id = term_component["terms_id"]
        term_component["terms_id"] = mapped_term_ids[source_term_id]
        replace_citations_ids(term_component, identifiers)
    for term_component in product_terms.get("cellularComponent", []):
        source_term_id = term_component["terms_id"]
        term_component["terms_id"] = mapped_term_ids[source_term_id]
        replace_citations_ids(term_component, identifiers)
    for term_component in product_terms.get("molecularFunction", []):
        source_term_id = term_component["terms_id"]
        term_component["terms_id"] = mapped_term_ids[source_term_id]
        replace_citations_ids(term_component, identifiers)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing organism_id
    replace_organism_id(json_object)


def promoter(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)
    '''
    # replacing promoter_feature_ids
    mapped_promoter_feature_ids = identifiers["promoterFeature"]
    for promoter_feature in json_object.get("promoterFeatures", []):
        source_promoter_feature_id = promoter_feature["promoterFeature_id"]
        promoter_feature["promoterFeature_id"] = mapped_promoter_feature_ids[source_promoter_feature_id]
        # replacing promoter feature citation_ids
        replace_citations_ids(promoter_feature, identifiers)

        # replacing bindsSigmaFactor citation_ids
        binds_sigma_factor = promoter_feature.get("bindsSigmaFactor", None)
        if binds_sigma_factor is not None:
            replace_citations_ids(binds_sigma_factor, identifiers)
    '''
    # replacing sigma_factor_id
    source_sigma_factor_id = json_object.get(
        "bindsSigmaFactor", {}).get("sigmaFactors_id", None)
    if source_sigma_factor_id is not None:
        mapped_sigma_factor_ids = identifiers["sigmaFactors"]
        json_object["bindsSigmaFactor"]["sigmaFactors_id"] = mapped_sigma_factor_ids[source_sigma_factor_id]
    # replacing sigma_factor_citations_evidence_id
    source_citations = json_object.get(
        "bindsSigmaFactor", {}).get("citations", None)
    if source_citations is not None:
        mapped_evidences_ids = identifiers["evidences"]
        mapped_publications_ids = identifiers["publications"]
        for citation in source_citations:
            if citation.get("evidences_id") is not None:
                citation["evidences_id"] = mapped_evidences_ids[citation["evidences_id"]]
            if citation.get("publications_id") is not None:
                citation["publications_id"] = mapped_publications_ids[citation["publications_id"]]

    # replacing organism_id
    replace_organism_id(json_object)


def publication(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing organism_id
    replace_organism_id(json_object)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)


def regulatory_complex(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing product ids
    mapped_product_ids = identifiers["products"]
    for product in json_object.get("products", []):
        source_product_id = product["products_id"]
        product["products_id"] = mapped_product_ids[source_product_id]

    # replacing regulatory_continuant ids
    mapped_regulatory_continuant_ids = identifiers["regulatoryContinuants"]
    for index, regulatory_continuant_id in enumerate(json_object.get("regulatoryContinuants_ids", [])):
        json_object["regulatoryContinuants_ids"][index] = mapped_regulatory_continuant_ids[regulatory_continuant_id]

    # replacing organism_id
    replace_organism_id(json_object)


def regulatory_continuant(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing organism_id
    replace_organism_id(json_object)


def regulatory_interaction(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing accessoryProteins
    mapped_proteins_ids = identifiers["regulatoryComplexes"]
    mapped_proteins_ids.update(identifiers["products"])

    new_proteins_ids = []
    for protein_id in json_object.get("accessoryProteins", []):
        new_proteins_ids.append(mapped_proteins_ids[protein_id])
    if new_proteins_ids != []:
        json_object["accessoryProteins"] = new_proteins_ids

    # replacing gene_id
    gene = json_object.get("gene", None)
    if gene is not None:
        mapped_gene_ids = identifiers["genes"]
        source_gene_id = gene["genes_id"]
        gene["genes_id"] = mapped_gene_ids[source_gene_id]

    # replacing promoter_id
    mapped_promoter_ids = identifiers["promoters"]
    for promoter in json_object.get("promoters", []):
        source_promoter_id = promoter["promoters_id"]
        promoter["promoters_id"] = mapped_promoter_ids[source_promoter_id]

    # replacing regulated_entity id
    regulated_entity = json_object.get("regulatedEntity", None)
    if regulated_entity is not None:
        regulated_entity_type = regulated_entity.get("type", None)
        source_regulated_entity_id = regulated_entity.get("_id", None)
        if regulated_entity_type == "gene":
            mapped_regulated_entity_ids = identifiers["genes"]
        elif regulated_entity_type == "transcriptionUnit":
            mapped_regulated_entity_ids = identifiers["transcriptionUnits"]
        else:
            mapped_regulated_entity_ids = identifiers["promoters"]
        json_object["regulatedEntity"]["_id"] = mapped_regulated_entity_ids[source_regulated_entity_id]

    # replacing regulator id
    regulator = json_object.get("regulator", None)
    if regulator is not None:
        regulator_type = regulator.get("type", None)
        source_regulator_entity_id = regulator.get("_id", None)
        if regulator_type == "product":
            mapped_regulator_entity_identifiers = identifiers["products"]
        elif regulator_type == "regulatoryComplex":
            mapped_regulator_entity_identifiers = identifiers["regulatoryComplexes"]
        else:
            mapped_regulator_entity_identifiers = identifiers["regulatoryContinuants"]
        json_object["regulator"]["_id"] = mapped_regulator_entity_identifiers[source_regulator_entity_id]

    # replacing gene_id
    binding_site_id = json_object.get(
        "regulatorySites_id", None)
    if binding_site_id is not None:
        mapped_binding_site_ids = identifiers["regulatorySites"]
        json_object["regulatorySites_id"] = mapped_binding_site_ids[binding_site_id]

    # replacing organism_id
    replace_organism_id(json_object)


def sigma_factor(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing gene ids
    mapped_gene_ids = identifiers["genes"]
    source_gene_id = json_object.get("genes_id", None)
    json_object["genes_id"] = mapped_gene_ids[source_gene_id]

    # replacing organism_id
    replace_organism_id(json_object)


def term(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing isA(parent terms) ids
    mapped_term_ids = identifiers["terms"]
    mapped_term_ids.update(identifiers["ontologies"])
    for index, term_id in enumerate(json_object.get("subClassOf", [])):
        json_object["subClassOf"][index] = mapped_term_ids[term_id]

    # replacing has(child terms) ids
    for index, term_id in enumerate(json_object.get("superClassOf", [])):
        json_object["superClassOf"][index] = mapped_term_ids[term_id]

    # replacing members's ids (genes and products)
    members = json_object.get("members", {})
    mapped_product_ids = identifiers["products"]
    for index, product_id in enumerate(members.get("products", [])):
        members["products"][index] = mapped_product_ids[product_id]
    mapped_gene_ids = identifiers["genes"]
    for index, gene_id in enumerate(members.get("genes", [])):
        members["genes"][index] = mapped_gene_ids[gene_id]

    # replacing ontology_id
    mapped_ontology_ids = identifiers["ontologies"]
    source_ontology_id = json_object.get("ontologies_id", None)
    if source_ontology_id is not None:
        json_object["ontologies_id"] = mapped_ontology_ids[source_ontology_id]

    # replacing organism_id
    replace_organism_id(json_object)


def terminator(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing organism_id
    replace_organism_id(json_object)


def transcription_unit(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)

    # replacing citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing gene ids
    mapped_gene_ids = identifiers["genes"]
    for index, gene_id in enumerate(json_object.get("genes_ids", [])):
        json_object["genes_ids"][index] = mapped_gene_ids[gene_id]

    # replacing operon ids
    mapped_operon_ids = identifiers["operons"]
    source_operon_id = json_object.get("operons_id", None)
    json_object["operons_id"] = mapped_operon_ids[source_operon_id]

    # replacing promoter id
    mapped_promoter_ids = identifiers["promoters"]
    source_promoter_id = json_object.get("promoters_id", None)
    if source_promoter_id is not None:
        json_object["promoters_id"] = mapped_promoter_ids[source_promoter_id]

    # replacing terminator_ids
    mapped_terminator_ids = identifiers["terminators"]
    for index, terminator_id in enumerate(json_object.get("terminators_ids", [])):
        json_object["terminators_ids"][index] = mapped_terminator_ids[terminator_id]

    # replacing organism_id
    replace_organism_id(json_object)


def transcription_factors(json_object, identifiers, collection_name):
    # replacing transcriptionFactorRegulatorySite_id
    mapped_site_identifiers = identifiers[collection_name]
    source_site_id = json_object.get("_id", None)
    json_object["_id"] = mapped_site_identifiers[source_site_id]
    # replacing site's external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)
    # replacing site's citation_ids
    replace_citations_ids(json_object, identifiers)

    # replacing active conformations
    mapped_product_ids = identifiers["products"]
    mapped_regulatory_complexes_ids = identifiers["regulatoryComplexes"]
    for index, active_conformation in enumerate(json_object.get("activeConformations", [])):
        if active_conformation["type"] == "product":
            active_conformation["_id"] = mapped_product_ids[active_conformation["_id"]]
        elif active_conformation["type"] == "regulatoryComplex":
            active_conformation["_id"] = mapped_regulatory_complexes_ids[active_conformation["_id"]]
    # replacing inactive conformations
    for index, inactive_conformation in enumerate(json_object.get("inactiveConformations", [])):
        inactive_conformation["_id"] = mapped_regulatory_complexes_ids[inactive_conformation["_id"]]
    # replacing organism_id
    replace_organism_id(json_object)

    # replacing products_id
    mapped_products_ids = identifiers["products"]
    new_products_ids = []
    for products_id in json_object.get("products_ids", []):
        new_products_ids.append(mapped_products_ids[products_id])
    json_object["products_ids"] = new_products_ids


def transcription_factor_regulatory_site(json_object, identifiers, collection_name):
    # replacing transcriptionFactorRegulatorySite_id
    mapped_site_identifiers = identifiers[collection_name]
    source_site_id = json_object.get("_id", None)
    json_object["_id"] = mapped_site_identifiers[source_site_id]
    # replacing site's external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)
    # replacing site's citation_ids
    replace_citations_ids(json_object, identifiers)
    # replacing organism_id
    replace_organism_id(json_object)


def segment(json_object, identifiers, collection_name):
    # replacing site's external_cross_reference_ids
    replace_external_cross_references_ids(json_object, identifiers)
    # replacing site's citation_ids
    replace_citations_ids(json_object, identifiers)


mg_replace_ids_builder = {
    "evidences": evidence,
    "externalCrossReferences": external_cross_references,
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
    "transcriptionUnits": transcription_unit,
    "transcriptionFactors": transcription_factors,
    "regulatorySites": transcription_factor_regulatory_site,
    "segments": segment
}


def replace_peak_id(json_object, identifiers, collection_name='peaks'):
    mapped_collection_ids = identifiers[collection_name]
    source_object_id = json_object["peakId"]
    json_object["peakId"] = mapped_collection_ids[source_object_id]


def replace_dataset_ids(json_object, identifiers):
    mapped_dataset_ids = identifiers["dataset"]
    dataset_ids = json_object.get("datasetIds", [])
    new_dataset_ids = []
    for dataset_id in dataset_ids:
        new_dataset_ids.append(mapped_dataset_ids[dataset_id])
    json_object["datasetIds"] = new_dataset_ids


def dataset(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)


def peaks(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing dataset_ids
    replace_dataset_ids(json_object, identifiers)


def tfBinding(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing dataset_ids
    replace_dataset_ids(json_object, identifiers)

    # replacing peakId
    replace_peak_id(json_object, identifiers, 'peaks')


def authors_data(json_object, identifiers, collection_name):
    replace_object_main_id(json_object, identifiers, collection_name)

    # replacing dataset_ids
    replace_dataset_ids(json_object, identifiers)


ht_replace_ids_builder = {
    "dataset": dataset,
    "peaks": peaks,
    "tfBinding": tfBinding,
    "authorsData": authors_data,
}
