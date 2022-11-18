from dataclasses import dataclass, field


@dataclass
class MetaboliteConsistent:
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
    def as_dict(self):
        return self.__dict__.copy()
