from sqlalchemy import Column, String, Float, Text, ARRAY, Integer, ForeignKey

from .sqlbase import EntityBase


class MetaboliteDiscoveryEntity(EntityBase):
    __tablename__ = 'mdb'

    # Primary Ids
    meta_id = Column(String(20), primary_key=True)

    chebi_ids = Column(ARRAY(String(20)))
    kegg_ids = Column(ARRAY(String(24)))
    lipidmaps_ids = Column(ARRAY(String(32)))
    pubchem_ids = Column(ARRAY(String(24)))
    hmdb_ids = Column(ARRAY(String(24)))
    cas_ids = Column(ARRAY(String(24)))

    def __init__(self, **kwargs):
        self.meta_id = kwargs.get('meta_id')
        self.chebi_ids = kwargs.get('chebi_ids')
        self.kegg_ids = kwargs.get('kegg_ids')
        self.lipidmaps_ids = kwargs.get('lipidmaps_ids')
        self.pubchem_ids = kwargs.get('pubchem_ids')
        self.hmdb_ids = kwargs.get('hmdb_ids')
        self.cas_ids = kwargs.get('cas_ids')
