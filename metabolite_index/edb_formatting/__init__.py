from .edb_specific import map_to_edb_format, flatten_hmdb_hierarchies,flatten_hmdb_hierarchies2, split_pubchem_ids
from .parsinglib import remap_keys, force_flatten, handle_names, strip_attr, flatten, MultiDict
from .padding import pad_id, depad_id, id_to_url


def preprocess(data: dict):
    handle_names(data)

    strip_attr(data, 'chebi_id', 'CHEBI:')
    strip_attr(data, 'hmdb_id', 'HMDB')
    strip_attr(data, 'lipidmaps_id', 'LM')
    strip_attr(data, 'inchi', 'InChI=')

    flatten(data, 'description')

__all__ = [
    'preprocess',
    'force_flatten',
    'MultiDict',
    'remap_keys', 'map_to_edb_format',
    'pad_id', 'depad_id', 'id_to_url',
    'flatten_hmdb_hierarchies', 'flatten_hmdb_hierarchies2', 'split_pubchem_ids'
]