from .edb_specific import map_to_edb_format, flatten_hmdb_hierarchies, split_pubchem_ids
from .parsinglib import remap_keys, force_list, force_flatten, handle_quotes, strip_attr, flatten, MultiDict
from .padding import pad_id, depad_id, id_to_url


def preprocess(data: dict):
    force_list(data, 'names')
    handle_quotes(data, 'names')

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
    'flatten_hmdb_hierarchies', 'split_pubchem_ids'
]