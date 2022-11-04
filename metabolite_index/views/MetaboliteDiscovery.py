from dataclasses import dataclass, field

from eme.mapper import map_to

from metabolite_index.views.MetaboliteConsistent import MetaboliteConsistent


@dataclass
class MetaboliteDiscovery:
    names: set[str] = field(default_factory=set)

    chebi_id: set[str] = field(default_factory=set)
    kegg_id: set[str] = field(default_factory=set)
    lipidmaps_id: set[str] = field(default_factory=set)
    pubchem_id: set[str] = field(default_factory=set)
    hmdb_id: set[str] = field(default_factory=set)
    cas_id: set[str] = field(default_factory=set)
    chemspider_id: set[str] = field(default_factory=set)
    metlin_id: set[str] = field(default_factory=set)

    # structures
    mol: set[str] = field(default_factory=set)
    formula: set[str] = field(default_factory=set)
    inchi: set[str] = field(default_factory=set)
    inchikey: set[str] = field(default_factory=set)
    smiles: set[str] = field(default_factory=set)

    # mass
    charge: set[float] = field(default_factory=set)
    mass: set[float] = field(default_factory=set)
    mi_mass: set[float] = field(default_factory=set)

    description: dict[str, str] = field(default_factory=dict)

    @property
    def primary_name(self):
        # @todo: policy to find primary_name ?
        return list(self.names)[0]

    def merge(self, other):
        if isinstance(other, MetaboliteDiscovery):
            for attr in self.__dict__:
                getattr(self, attr).update(getattr(other, attr))
        else:
            # try to map obj to MetaboliteConsistent and then merge
            mapped_obj = map_to(other, cls_dest=MetaboliteDiscovery)
            return self.merge(mapped_obj)

    def __repr__(self):
        sb = [self.__class__.__name__]

        for attr, vals in self.__dict__.items():
            desomsz = ', '.join(vals)
            sb.append(f'  {attr:<16}: {desomsz}')

        return '\n'.join(sb)
