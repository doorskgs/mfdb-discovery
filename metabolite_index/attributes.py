
"""
Common non-ID attributes shared by all major EDBs
"""
from enum import Enum

COMMON_ATTRIBUTES = {
    "names", "description",
    'formula', 'inchi', 'inchikey', 'smiles',
    'mass', 'mi_mass', "charge"
}


class EDBSource(Enum):

    pubchem = 'pubchem'
    chebi = 'chebi'
    hmdb = 'hmdb'
    kegg = 'kegg'
    lipidmaps = 'lipidmaps'

"""
EDBs supported
"""
EDB_SOURCES = set(map(lambda x: x.value, iter(EDBSource)))

def is_supported(reftag: str | tuple[str, str]):
    if isinstance(reftag, tuple) and len(reftag)==2:
        reftag = reftag[0]

    if reftag.endswith('_id'):
        reftag = reftag[:-3]

    return reftag in EDB_SOURCES

EDB_SOURCES_OTHER = { 'cas', 'chemspider', 'metlin', 'swisslipids' }

# 'chembl_id',

#   'metabolights_id',
# 'chebi_id_alt', 'hmdb_id_alt', 'pubchem_sub_id',
# #'pdb_id', 'uniprot_id',
# 'drugbank_id', 'kegg_drug_id',
# 'wiki_id',
# 'pubmed_id',

"""
List of EDB_IDs that are not yet supported by MFDB, but are well known
Also includes non-metabolite refs, like protein DBs
"""
EDB_ID_OTHER = set(map(lambda x: x+'_id', iter(EDB_SOURCES_OTHER)))
