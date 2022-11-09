from dataclasses import dataclass, field

from metabolite_index.edb_formatting import TrimSet, strip_attr
from eme.mapper import map_to



@dataclass
class MetaboliteDiscovery:
    names: set[str] = field(default_factory=TrimSet)

    chebi_id: set[str] = field(default_factory=TrimSet)
    kegg_id: set[str] = field(default_factory=TrimSet)
    lipidmaps_id: set[str] = field(default_factory=TrimSet)
    pubchem_id: set[str] = field(default_factory=TrimSet)
    hmdb_id: set[str] = field(default_factory=lambda: TrimSet(trimmer=lambda x: strip_attr(x, 'HMDB')))
    cas_id: set[str] = field(default_factory=TrimSet)
    chemspider_id: set[str] = field(default_factory=TrimSet)
    metlin_id: set[str] = field(default_factory=TrimSet)

    # structures
    mol: set[str] = field(default_factory=TrimSet)
    formula: set[str] = field(default_factory=TrimSet)
    inchi: set[str] = field(default_factory=TrimSet)
    inchikey: set[str] = field(default_factory=TrimSet)
    smiles: set[str] = field(default_factory=TrimSet)

    # mass
    charge: set[float] = field(default_factory=TrimSet)
    mass: set[float] = field(default_factory=TrimSet)
    mi_mass: set[float] = field(default_factory=TrimSet)

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
            desomsz = ' • '.join(map(str, vals))
            sb.append(f'  {attr:<16}: {desomsz}')

        return '\n'.join(sb)
