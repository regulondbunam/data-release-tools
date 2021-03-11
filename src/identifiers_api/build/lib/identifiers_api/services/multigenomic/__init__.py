from . import evidence
from . import external_cross_reference
from . import gene
from . import motif
from . import operon
from . import organism
from . import product
from . import promoter
from . import publication
from . import regulatory_complex
from . import regulatory_continuant
from . import regulatory_interaction
from . import sigma_factor
from . import term
from . import terminator
from . import transcription_unit
from ..shared import base


def get_identifiers(identifier_type, regulondb_database, organism):
    return base.get_all(identifier_type, regulondb_database, organism)