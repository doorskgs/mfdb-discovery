from .parsinglib import force_flatten, try_flatten, strip_attr, handle_names, flatten
from ..attributes import  EDB_SOURCES, EDB_ID_OTHER, COMMON_ATTRIBUTES
from .structs import MultiDict


EDB_IDS = set(map(lambda x:x+'_id', EDB_SOURCES))

def map_to_edb_format(me: dict, important_attr: set):
    """
    Parses EDB dictionary (from bulk dump files) to universal EDB format accepted by MetaboliteExternal

    :param me: data dict to be transformed
    :param important_attr: attributes that are important to be marked for this EDB
    :return: dict
    """
    out = {}
    attr_mul = MultiDict()
    attr_other = MultiDict()

    # these attributes are copied as-is, they're ok to be non-scalar
    out["names"] = me.pop("names", [])

    # force scalar and store redundant ids/attributes
    for _key in (EDB_IDS | COMMON_ATTRIBUTES | EDB_ID_OTHER) - {"names"}:
        if val := me.pop(_key, None):
            out[_key] = force_flatten(val, redundant_values := [])

            if redundant_values:
                attr_mul.extend(_key, redundant_values)

    for _key in important_attr:
        if val := me.pop(_key, None):
            # todo: should we best-effort flatten other attributes OR force flatten them?
            attr_other.extend(_key, try_flatten(val))

    out["attr_mul"] = dict(attr_mul)
    out["attr_other"] = dict(attr_other)

    return out, dict(me)


def split_pubchem_ids(r):
    sids = []

    if 'pubchem_id' in r:
        if not isinstance(r['pubchem_id'], (list, tuple, set)):
            r['pubchem_id'] = [strip_attr(r['pubchem_id'], 'CID:')]

        # filter out substance IDs and flatten remaining IDs if possible
        sids = list(filter(lambda x: x.startswith("SID:"), r['pubchem_id']))
        r['pubchem_id'] = strip_attr(try_flatten(list(filter(lambda x: not x.startswith("SID:"), r['pubchem_id']))), 'CID:')

    return sids


def replace_obvious_hmdb_id(hmdb_id):
    if len(hmdb_id) == 9:
        return hmdb_id[:4]+'00'+hmdb_id[4:]

    return hmdb_id

def preprocess(data: dict):
    handle_names(data)

    data['chebi_id'] = strip_attr(data['chebi_id'], 'CHEBI:')
    data['hmdb_id'] = strip_attr(data['hmdb_id'], 'HMDB')
    data['lipidmaps_id'] = strip_attr(data['lipidmaps_id'], 'LM')
    data['inchi'] = strip_attr(data['inchi'], 'InChI=')

    flatten(data, 'description')

def flatten_hmdb_hierarchies2(r: MultiDict):
    # Secondary IDs
    secondary = r.pop('secondary_accessions', None)
    if secondary:
        r.extend('hmdb_id_alt', secondary['secondary_accessions.accession'])

    # Synonyms
    synonyms = r.pop('synonyms', None)
    if synonyms:
        r.extend('names', synonyms['synonyms.synonym'])

