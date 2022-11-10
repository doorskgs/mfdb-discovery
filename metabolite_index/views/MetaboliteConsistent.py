from dataclasses import dataclass, field


@dataclass
class MetaboliteConsistent:
    edb_source: str
    names: list[str]

    # extra refs
    #pdb_id: list[str]
    attr_mul: dict[str, list[str]]# EDB IDs and attributes with cardinality > 1
    attr_other: dict[str, list[str] | str] # other marked attributes and other well known IDS

    chebi_id: str = None
    kegg_id: str = None
    lipmaps_id: str = None
    pubchem_id: str = None
    hmdb_id: str = None

    cas_id: str = None
    chemspider_id: str = None
    metlin_id: str = None
    swisslipids_id: str = None

    # structures
    #mol: str = None
    formula: str = None
    inchi: str = None
    inchikey: str = None
    smiles: str = None

    # mass
    charge: float = None
    mass: float = None
    mi_mass: float = None# monoisotopic mass

    description: str = None

    @property
    def primary_name(self):
        # @todo: policy to find primary_name ?
        return list(self.names)[0]

    @property
    def edb_id(self):
        if self.edb_source == 'chebi':
            return self.chebi_id
        elif self.edb_source == 'hmdb':
            return self.hmdb_id
        elif self.edb_source == 'lipmaps' or self.edb_source == 'lipidmaps':
            return self.lipmaps_id
        elif self.edb_source == 'kegg':
            return self.kegg_id
        elif self.edb_source == 'pubchem':
            return self.pubchem_id
        elif self.edb_source == 'metlin':
            return self.metlin_id
        elif self.edb_source == 'chemspider':
            return self.chemspider_id
        else:
            raise Exception("unsupported source format")

    @property
    def as_dict(self):
        return self.__dict__.copy()
