from identifiers_api.services import base


def get_all() -> [base.Identifier]:
    return base.get_all(regulondb_type="geneExpressionContrast", database="regulondbht")


def find_by_id(id_: str) -> base.Identifier:
    return base.find_one_by_id(id_, regulondb_type="geneExpressionContrast", database="regulondbht")

