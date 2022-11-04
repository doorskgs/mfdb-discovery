from eme.mapper import Mapping

from ..dal.entities.ExternalDBEntity import ExternalDBEntity
from metabolite_index.edb_formatting import force_flatten
from ..views.MetaboliteConsistent import MetaboliteConsistent


@Mapping(ExternalDBEntity, MetaboliteConsistent)
def edb2disco(mapper):
    mapper.for_member('names', lambda opt: opt.names)

    #mapper.for_member('description', lambda opt: {'any': opt.description})


@Mapping(MetaboliteConsistent, ExternalDBEntity)
def edb2disco(mapper):
    # @note: this mapping isn't really used
    mapper.for_member('names', lambda opt: opt.names)

    mapper.for_member('edb_id', ExternalDBEntity.edb_id)
    mapper.for_member('edb_source', ExternalDBEntity.edb_source)
    mapper.for_member('chebi_id', ExternalDBEntity.chebi_id)
    mapper.for_member('kegg_id', ExternalDBEntity.kegg_id)
    mapper.for_member('lipidmaps_id', ExternalDBEntity.lipidmaps_id)
    mapper.for_member('pubchem_id', ExternalDBEntity.pubchem_id)
    mapper.for_member('hmdb_id', ExternalDBEntity.hmdb_id)

    mapper.for_member('cas_id', ExternalDBEntity.cas_id)
    mapper.for_member('chemspider_id', ExternalDBEntity.chemspider_id)
    mapper.for_member('metlin_id', ExternalDBEntity.metlin_id)

    mapper.for_member('smiles', ExternalDBEntity.smiles)
    mapper.for_member('inchi', ExternalDBEntity.inchi)
    mapper.for_member('inchikey', ExternalDBEntity.inchikey)
    mapper.for_member('formula', ExternalDBEntity.formula)
    mapper.for_member('charge', ExternalDBEntity.charge)
    mapper.for_member('mass', ExternalDBEntity.mass)
    mapper.for_member('mi_mass', ExternalDBEntity.mi_mass)

    mapper.for_member('attr_mul', ExternalDBEntity.attr_mul)
    mapper.for_member('attr_other', ExternalDBEntity.attr_other)
