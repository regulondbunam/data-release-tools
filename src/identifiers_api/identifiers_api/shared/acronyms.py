from identifiers_api.shared.constants import *


def get_db_acronym(identifiers_object):
    database = identifiers_object.get("regulondbDatabase", None)
    if database in REGULONDB_DATABASES_ACRONYMS:
        return REGULONDB_DATABASES_ACRONYMS[database]
    return "RDB"
