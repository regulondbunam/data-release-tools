import mongoengine

from identifiers_api.shared import constants
from identifiers_api.services.identifiers import create_id
from identifiers_api.services.identifiers import get_identifiers
from identifiers_api.services.identifiers import update_id
from identifiers_api.services import regulondbmultigenomic


def connect(uri, database="regulondbidentifiers"):
    mongoengine.connect(database, host=uri)


def disconnect():
    mongoengine.disconnect()