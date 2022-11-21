from eme.mapper import Mapping

from ..dal.entities.ExternalDBEntity import ExternalDBEntity
from ..views.MetaboliteConsistent import MetaboliteConsistent


@Mapping(ExternalDBEntity, MetaboliteConsistent)
def entity2consistent(mapper):
    """
    Maps Metabolite consistent object to entity
    (added for external library purposes; not used in discovery algorithm)

    :param mapper:
    :return:
    """

    # todo: handle description
    # todo: handle mol file

    mapper.for_member(ExternalDBEntity.names, 'names')
    mapper.for_member(ExternalDBEntity.description, mapper.ignore())

    mapper.for_member(ExternalDBEntity.edb_id, 'edb_id')
    mapper.for_member(ExternalDBEntity.edb_source, 'edb_source')

    mapper.for_member(ExternalDBEntity.chebi_id, 'chebi_id')
    mapper.for_member(ExternalDBEntity.kegg_id, 'kegg_id')
    mapper.for_member(ExternalDBEntity.lipmaps_id, 'lipmaps_id')
    mapper.for_member(ExternalDBEntity.pubchem_id, 'pubchem_id')
    mapper.for_member(ExternalDBEntity.hmdb_id, 'hmdb_id')

    mapper.for_member(ExternalDBEntity.cas_id, 'cas_id')
    mapper.for_member(ExternalDBEntity.chemspider_id, 'chemspider_id')
    mapper.for_member(ExternalDBEntity.metlin_id, 'metlin_id')

    mapper.for_member(ExternalDBEntity.smiles, 'smiles')
    mapper.for_member(ExternalDBEntity.inchi, 'inchi')
    mapper.for_member(ExternalDBEntity.inchikey, 'inchikey')
    mapper.for_member(ExternalDBEntity.formula, 'formula')
    mapper.for_member(ExternalDBEntity.charge, 'charge')
    mapper.for_member(ExternalDBEntity.mass, 'mass')
    mapper.for_member(ExternalDBEntity.mi_mass, 'mi_mass')

    mapper.for_member(ExternalDBEntity.attr_mul, 'attr_mul')
    mapper.for_member(ExternalDBEntity.attr_other, 'attr_other')



@Mapping(MetaboliteConsistent, ExternalDBEntity)
def consistent2entity(mapper):
    # @UNUSED
    return

    mapper.for_member('names', ExternalDBEntity.names)
    mapper.for_member('description', mapper.ignore())

    mapper.for_member('edb_id', ExternalDBEntity.edb_id)
    mapper.for_member('edb_source', ExternalDBEntity.edb_source)

    mapper.for_member('chebi_id', ExternalDBEntity.chebi_id)
    mapper.for_member('kegg_id', ExternalDBEntity.kegg_id)
    mapper.for_member('lipmaps_id', ExternalDBEntity.lipmaps_id)
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
