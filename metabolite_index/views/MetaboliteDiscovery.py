from dataclasses import dataclass, field

from metabolite_index.consistency import get_discovery_attribute_consistencies, ConsistencyClass
from metabolite_index.edb_formatting.structs import repr_set, AlmostEqualSet, TrimSet
from metabolite_index.edb_formatting import strip_attr, pad_id
from eme.mapper import map_to



@dataclass
class MetaboliteDiscovery:
    names: set[str] = field(default_factory=TrimSet)

    chebi_id: set[str] = field(default_factory=lambda: TrimSet(trimmer=lambda x: strip_attr(x, 'CHEBI:')))
    kegg_id: set[str] = field(default_factory=TrimSet)
    lipmaps_id: set[str] = field(default_factory=lambda: TrimSet(trimmer=lambda x: strip_attr(x, 'LM')))
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
    mass: set[float] = field(default_factory=AlmostEqualSet)
    mi_mass: set[float] = field(default_factory=AlmostEqualSet)

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
        repr_dict = dict(self.__dict__)

        repr_dict['hmdb_id'] = set(pad_id(s, 'hmdb_id') for s in repr_dict['hmdb_id'])
        repr_dict['chebi_id'] = set(pad_id(s, 'chebi_id') for s in repr_dict['chebi_id'])
        repr_dict['lipmaps_id'] = set(pad_id(s, 'lipmaps_id') for s in repr_dict['lipmaps_id'])

        repr_dict['mass'] = repr_dict['mass'].equivalence_set
        repr_dict['mi_mass'] = repr_dict['mi_mass'].equivalence_set

        consistencies = get_discovery_attribute_consistencies(self)

        for attr, vals in repr_dict.items():
            c = consistencies.get(attr, ConsistencyClass.Consistent)

            sb.append(f'  {attr:<16}: {str(c)} {repr_set(vals)}')

        return '\n'.join(sb)
