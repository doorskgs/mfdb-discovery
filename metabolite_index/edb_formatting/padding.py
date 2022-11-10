from metabolite_index.edb_formatting.parsinglib import try_flatten

_PADDINGS = {
    'hmdb_id': 'HMDB',
    'chebi_id': 'CHEBI:',
    #'kegg_id': 'C',
    'lipmaps_id': 'LM',
    'inchi': 'InChI='
}

def strip_attr(v: list | set | str, prefix):
    if not v:
        return v

    if isinstance(v, list):
        return list(map(lambda v: v.removeprefix(prefix).lstrip(), v))
    else:
        return v.removeprefix(prefix).lstrip()

def strip_prefixes(data: dict):
    for edb_tag, prefix in _PADDINGS.items():
        data[edb_tag] = strip_attr(data[edb_tag], prefix)

def guess_db(db_id: str):
    for db_tag, _pad in _PADDINGS.items():
        if db_id.startswith(_pad):
            return db_tag


def id_to_url(db_id, db_tag=None):
    if db_tag is None:
        db_tag = guess_db(db_id)
        if db_tag is None:
            return None

    db_id = pad_id(db_id, db_tag)
    url = None

    if db_tag == 'hmdb_id':
        url = f"https://hmdb.ca/metabolites/{db_id}"
    elif db_tag == 'chebi_id':
        url = f"https://www.ebi.ac.uk/chebi/searchId.do;?chebiId={db_id}"
    elif db_tag == 'kegg_id':
        url = f"https://www.genome.jp/dbget-bin/www_bget?cpd:{db_id}"
    elif db_tag == 'pubchem_id':
        url = f"https://pubchem.ncbi.nlm.nih.gov/compound/{db_id}"
    elif db_tag == 'lipmaps_id':
        url = f"https://www.lipidmaps.org/data/LMSDRecord.php?LMID={db_id}"

    return url


def depad_id(db_id, db_tag=None):
    if db_id is None:
        return None

    if db_tag is None:
        db_tag = guess_db(db_id)

        if db_tag is None:
            raise Exception("db_tag not provided for depad_id. How couldst i depad yond hast mere db tag?")

    padding = _PADDINGS.get(db_tag)

    if padding is not None and db_id.startswith(padding):
        return db_id[len(padding):]
    return db_id


def pad_id(db_id, db_tag):
    padding = _PADDINGS.get(db_tag)

    if padding is None or db_id.startswith(padding):
        _id = str(db_id)
    else:
        _id = padding+db_id

    return _id


def split_pubchem_ids(r):
    sids = []

    if 'pubchem_id' in r:
        if not isinstance(r['pubchem_id'], (list, tuple, set)):
            r['pubchem_id'] = [strip_attr(r['pubchem_id'], 'CID:')]

        # filter out substance IDs and flatten remaining IDs if possible
        sids = list(filter(lambda x: x.startswith("SID:"), r['pubchem_id']))
        r['pubchem_id'] = strip_attr(try_flatten(list(filter(lambda x: not x.startswith("SID:"), r['pubchem_id']))), 'CID:')

    return sids
