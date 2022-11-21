from eme.mapper import Mapping

from ..edb_formatting import force_flatten
from ..views.MetaboliteConsistent import MetaboliteConsistent
from ..views.MetaboliteDiscovery import MetaboliteDiscovery


@Mapping(MetaboliteConsistent, MetaboliteDiscovery)
def consistent2disco(mapper):
    """
    Maps MetaboliteConsistent to Discovery object
    (added for library purposes)

    :param mapper:
    :return:
    """
    # TODO: @later: add description into JSON like {edb_source -> descript}

    # TODO: store attr other in MetaboliteDiscovery?

    # TODO: store mol file

    def extra_ref(n, opt):
        return set(opt.attr_mul.get(n, []))

    mapper.for_member('names', lambda opt: opt.names)
    mapper.for_member('description', mapper.ignore())

    mapper.for_member('chebi_id', lambda opt: {opt.chebi_id} | extra_ref('chebi_id', opt))
    mapper.for_member('kegg_id', lambda opt: {opt.kegg_id} | extra_ref('kegg_id', opt))
    mapper.for_member('lipmaps_id', lambda opt: {opt.lipmaps_id} | extra_ref('lipmaps_id', opt))
    mapper.for_member('pubchem_id', lambda opt: {opt.pubchem_id} | extra_ref('pubchem_id', opt))
    mapper.for_member('hmdb_id', lambda opt: {opt.hmdb_id} | extra_ref('hmdb_id', opt))

    mapper.for_member('cas_id', lambda opt: {opt.cas_id} | extra_ref('cas_id', opt))
    mapper.for_member('chemspider_id', lambda opt: {opt.chemspider_id} | extra_ref('chemspider_id', opt))
    mapper.for_member('metlin_id', lambda opt: {opt.metlin_id} | extra_ref('metlin_id', opt))

    mapper.for_member('formula', lambda opt: {opt.formula} | extra_ref('formula', opt))
    mapper.for_member('inchi', lambda opt: {opt.inchi} | extra_ref('inchi', opt))
    mapper.for_member('inchikey', lambda opt: {opt.inchikey} | extra_ref('inchikey', opt))
    mapper.for_member('smiles', lambda opt: {opt.smiles} | extra_ref('smiles', opt))

    mapper.for_member('charge', lambda opt: {opt.charge} | extra_ref('charge', opt))
    mapper.for_member('mass', lambda opt: {opt.mass} | extra_ref('mass', opt))
    mapper.for_member('mi_mass', lambda opt: {opt.mi_mass} | extra_ref('mi_mass', opt))

    mapper.for_member('mol', mapper.ignore())


@Mapping(MetaboliteDiscovery, MetaboliteConsistent)
def disco2consistent(mapper):
    """
    Maps Discovery object to Consistent metabolite object
    (added for library purposes - e.g. used in serializing bulk discovery)

    :param mapper:
    :return:
    """

    # todo: handle description later
    # todo: handle mol files later
    # todo: handle other attributes later

    mapper.for_member('names', lambda opt: opt.names)
    mapper.for_member('description', mapper.ignore())

    mapper.for_member('chebi_id', lambda opt: force_flatten(opt.chebi_id, opt.attr_mul))
    mapper.for_member('kegg_id', lambda opt: force_flatten(opt.kegg_id, opt.attr_mul))
    mapper.for_member('lipmaps_id', lambda opt: force_flatten(opt.lipmaps_id, opt.attr_mul))
    mapper.for_member('pubchem_id', lambda opt: force_flatten(opt.pubchem_id, opt.attr_mul))
    mapper.for_member('hmdb_id', lambda opt: force_flatten(opt.hmdb_id, opt.attr_mul))

    mapper.for_member('cas_id', lambda opt: force_flatten(opt.cas_id, opt.attr_mul))
    mapper.for_member('chemspider_id', lambda opt: force_flatten(opt.chemspider_id, opt.attr_mul))
    mapper.for_member('metlin_id', lambda opt: force_flatten(opt.metlin_id, opt.attr_mul))

    mapper.for_member('smiles', lambda opt: force_flatten(opt.smiles, opt.attr_mul))
    mapper.for_member('inchi', lambda opt: force_flatten(opt.inchi, opt.attr_mul))
    mapper.for_member('inchikey', lambda opt: force_flatten(opt.inchikey, opt.attr_mul))
    mapper.for_member('formula', lambda opt: force_flatten(opt.formula, opt.attr_mul))
    mapper.for_member('charge', lambda opt: force_flatten(opt.charge, opt.attr_mul))
    mapper.for_member('mass', lambda opt: force_flatten(opt.mass, opt.attr_mul))
    mapper.for_member('mi_mass', lambda opt: force_flatten(opt.mi_mass, opt.attr_mul))

    mapper.for_member('mol', mapper.ignore())
