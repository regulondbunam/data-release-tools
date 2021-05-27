from identifiers_api.services import base


def evidence():
    pass


def get_all() -> [base.Identifier]:
    return base.get_all(regulondb_type="evidence", database="regulondbmultigenomic")


def find_by_id(id_: str) -> base.Identifier:
    return base.find_one_by_id(id_, regulondb_type="evidence", database="regulondbmultigenomic")


def create_id(evidence: dict, regulondb_version: str):
    pass


def create_ids(evidence: [dict], regulondb_version: str):
    pass

