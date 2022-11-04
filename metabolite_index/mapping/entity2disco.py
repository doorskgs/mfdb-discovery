from eme.mapper import Mapping

from ..dal.entities.ExternalDBEntity import ExternalDBEntity
from metabolite_index.edb_formatting import force_flatten
from ..views.MetaboliteDiscovery import MetaboliteDiscovery


@Mapping(ExternalDBEntity, MetaboliteDiscovery)
def edb2disco(mapper):
    mapper.for_member('names', lambda opt: opt.names)

    # todO: @later: add description into JSON like {edb_source -> descript}
    mapper.for_member('description', lambda opt: {'any': opt.description})

    def extra_ref(n, opt):
        return set(opt.attr_mul.get(n, []))

    # todo: store attr other in MetaboliteDiscovery?

    mapper.for_member('chebi_id', lambda opt: {opt.chebi_id} & extra_ref('chebi_id', opt))
    mapper.for_member('kegg_id', lambda opt: {opt.kegg_id} & extra_ref('kegg_id', opt))
    mapper.for_member('lipidmaps_id', lambda opt: {opt.lipidmaps_id} & extra_ref('lipidmaps_id', opt))
    mapper.for_member('pubchem_id', lambda opt: {opt.pubchem_id} & extra_ref('pubchem_id', opt))
    mapper.for_member('hmdb_id', lambda opt: {opt.hmdb_id} & extra_ref('hmdb_id', opt))

    mapper.for_member('cas_id', lambda opt: {opt.cas_id} & extra_ref('cas_id', opt))
    mapper.for_member('chemspider_id', lambda opt: {opt.chemspider_id} & extra_ref('chemspider_id', opt))
    mapper.for_member('metlin_id', lambda opt: {opt.metlin_id} & extra_ref('metlin_id', opt))

    #mapper.for_member('mol', lambda opt: {opt.mol} & extra_ref('mol', opt))
    mapper.for_member('formula', lambda opt: {opt.formula} & extra_ref('formula', opt))
    mapper.for_member('inchi', lambda opt: {opt.inchi} & extra_ref('inchi', opt))
    mapper.for_member('inchikey', lambda opt: {opt.inchikey} & extra_ref('inchikey', opt))
    mapper.for_member('smiles', lambda opt: {opt.smiles} & extra_ref('smiles', opt))

    mapper.for_member('charge', lambda opt: {opt.charge} & extra_ref('charge', opt))
    mapper.for_member('mass', lambda opt: {opt.mass} & extra_ref('mass', opt))
    mapper.for_member('mi_mass', lambda opt: {opt.mi_mass} & extra_ref('mi_mass', opt))



@Mapping(MetaboliteDiscovery, ExternalDBEntity)
def edb2disco(mapper):
    # @note: this mapping isn't really used

    # mapper.for_member(ExternalDBEntity.names, lambda opt: set(json.loads(opt)))
    # todo: handle description later
    #mapper.for_member(ExternalDBEntity.description, )

    mapper.for_member(ExternalDBEntity.edb_id, lambda opt: force_flatten(opt.edb_id, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.edb_source, lambda opt: force_flatten(opt.edb_source, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.chebi_id, lambda opt: force_flatten(opt.chebi_id, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.kegg_id, lambda opt: force_flatten(opt.kegg_id, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.lipidmaps_id, lambda opt: force_flatten(opt.lipidmaps_id, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.pubchem_id, lambda opt: force_flatten(opt.pubchem_id, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.hmdb_id, lambda opt: force_flatten(opt.hmdb_id, opt.attr_mul))

    mapper.for_member(ExternalDBEntity.cas_id, lambda opt: force_flatten(opt.cas_id, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.chemspider_id, lambda opt: force_flatten(opt.chemspider_id, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.metlin_id, lambda opt: force_flatten(opt.metlin_id, opt.attr_mul))

    mapper.for_member(ExternalDBEntity.smiles, lambda opt: force_flatten(opt.smiles, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.inchi, lambda opt: force_flatten(opt.inchi, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.inchikey, lambda opt: force_flatten(opt.inchikey, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.formula, lambda opt: force_flatten(opt.formula, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.charge, lambda opt: force_flatten(opt.charge, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.mass, lambda opt: force_flatten(opt.mass, opt.attr_mul))
    mapper.for_member(ExternalDBEntity.mi_mass, lambda opt: force_flatten(opt.mi_mass, opt.attr_mul))
