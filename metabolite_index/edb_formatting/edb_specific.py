from metabolite_index import EDB_SOURCES, EDB_ID_OTHER, COMMON_ATTRIBUTES

from .parsinglib import force_flatten, try_flatten, strip_attr, MultiDict

EDB_IDS = set(map(lambda x:x+'_id', EDB_SOURCES))

def map_to_edb_format(me: dict, important_attr: set):
    """
    Parses EDB dictionary (from bulk dump files) to universal EDB format accepted by MetaboliteExternal

    :param me: data dict to be transformed
    :param important_attr: attributes that are important to be marked for this EDB
    :return: dict
    """
    out = {}
    attr_mul = {}
    attr_other = {}

    # these attributes are copied as-is, they're ok to be non-scalar
    out["names"] = me.pop("names", [])

    # force scalar and store redundant ids/attributes
    for _key in (EDB_IDS | COMMON_ATTRIBUTES | EDB_ID_OTHER) - {"names"}:
        if val := me.pop(_key, None):
            out[_key] = force_flatten(val, redundant_values := [])

            if redundant_values:
                attr_mul[_key] = redundant_values

    for _key in important_attr:
        if val := me.pop(_key, None):
            # todo: should we best-effort flatten other attributes OR force flatten them?
            attr_other[_key] = try_flatten(val)

    out["attr_mul"] = attr_mul
    out["attr_other"] = attr_other

    return out, dict(me)


def split_pubchem_ids(r):
    sids = []

    if 'pubchem_id' in r:
        strip_attr(r, 'pubchem_id', 'CID:')

        if not isinstance(r['pubchem_id'], (list, tuple, set)):
            r['pubchem_id'] = [r['pubchem_id']]

        # filter out substance IDs and flatten remaining IDs if possible
        sids = list(filter(lambda x: x.startswith("SID:"), r['pubchem_id']))
        r['pubchem_id'] = try_flatten(list(filter(lambda x: not x.startswith("SID:"), r['pubchem_id'])))

    return sids


def flatten_hmdb_hierarchies(r):
    raise NotImplementedError()
    if 'synonyms' in r:
        synsyn = r.pop('synonyms')

        if synsyn:
            if isinstance(synsyn, list) and synsyn[0]:
                r['names'].extend(synsyn[0]['synonym'])
            elif isinstance(synsyn, dict):
                r['names'].extend(synsyn['synonyms.synonym'])
    elif 'names' in r:
        for i,syn in enumerate(r['names']):
            if isinstance(syn, dict):
                r['names'][i] = syn['synonym']

    if 'secondary_accessions' in r:
        accacc = r.pop('secondary_accessions')

        if accacc and accacc[0]:
            r['hmdb_id_alt'].extend(accacc[0]['accession'])
    elif 'hmdb_id_alt' in r:
        for i, syn in enumerate(r['hmdb_id_alt']):
            if isinstance(syn, dict):
                r['hmdb_id_alt'][i] = syn['accession']

def flatten_hmdb_hierarchies2(r: MultiDict):
    # Secondary IDs
    secondary = r.pop('secondary_accessions', None)
    if secondary:
        r.extend('hmdb_id_alt', secondary['secondary_accessions.accession'])

    # Synonyms
    synonyms = r.pop('synonyms', None)
    if synonyms:
        r.extend('names', synonyms['synonyms.synonym'])

