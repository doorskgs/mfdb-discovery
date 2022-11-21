from eme.mapper import Mapping

from ..dal.entities.ExternalDBEntity import ExternalDBEntity
from ..dal.entities.MetaboliteDBEntity import MetaboliteDBEntity


@Mapping(ExternalDBEntity, MetaboliteDBEntity)
def edb2mdb(mapper):
    #@UNUSED
    raise NotImplementedError()

    mapper.for_member(ExternalDBEntity.names, MetaboliteDBEntity.names)

    mapper.for_member(ExternalDBEntity.edb_id, MetaboliteDBEntity.edb_id)
    mapper.for_member(ExternalDBEntity.edb_source, MetaboliteDBEntity.edb_source)

    mapper.for_member(ExternalDBEntity.chebi_id, MetaboliteDBEntity.chebi_id)
    mapper.for_member(ExternalDBEntity.kegg_id, MetaboliteDBEntity.kegg_id)
    mapper.for_member(ExternalDBEntity.lipmaps_id, MetaboliteDBEntity.lipmaps_id)
    mapper.for_member(ExternalDBEntity.pubchem_id, MetaboliteDBEntity.pubchem_id)
    mapper.for_member(ExternalDBEntity.hmdb_id, MetaboliteDBEntity.hmdb_id)

    mapper.for_member(ExternalDBEntity.cas_id, MetaboliteDBEntity.cas_id)
    mapper.for_member(ExternalDBEntity.chemspider_id, MetaboliteDBEntity.chemspider_id)
    mapper.for_member(ExternalDBEntity.metlin_id, MetaboliteDBEntity.metlin_id)

    mapper.for_member(ExternalDBEntity.smiles, MetaboliteDBEntity.smiles)
    mapper.for_member(ExternalDBEntity.inchi, MetaboliteDBEntity.inchi)
    mapper.for_member(ExternalDBEntity.inchikey, MetaboliteDBEntity.inchikey)
    mapper.for_member(ExternalDBEntity.formula, MetaboliteDBEntity.formula)
    mapper.for_member(ExternalDBEntity.charge, MetaboliteDBEntity.charge)
    mapper.for_member(ExternalDBEntity.mass, MetaboliteDBEntity.mass)
    mapper.for_member(ExternalDBEntity.mi_mass, MetaboliteDBEntity.mi_mass)

    mapper.for_member(ExternalDBEntity.attr_mul, MetaboliteDBEntity.attr_mul)
    mapper.for_member(ExternalDBEntity.attr_other, MetaboliteDBEntity.attr_other)


@Mapping(MetaboliteDBEntity, ExternalDBEntity)
def mdb2edb(mapper):
    #@UNUSED
    raise NotImplementedError()

    mapper.for_member(MetaboliteDBEntity.names, ExternalDBEntity.names)

    mapper.for_member(MetaboliteDBEntity.edb_id, ExternalDBEntity.edb_id)
    mapper.for_member(MetaboliteDBEntity.edb_source, ExternalDBEntity.edb_source)

    mapper.for_member(MetaboliteDBEntity.chebi_id, ExternalDBEntity.chebi_id)
    mapper.for_member(MetaboliteDBEntity.kegg_id, ExternalDBEntity.kegg_id)
    mapper.for_member(MetaboliteDBEntity.lipmaps_id, ExternalDBEntity.lipmaps_id)
    mapper.for_member(MetaboliteDBEntity.pubchem_id, ExternalDBEntity.pubchem_id)
    mapper.for_member(MetaboliteDBEntity.hmdb_id, ExternalDBEntity.hmdb_id)

    mapper.for_member(MetaboliteDBEntity.cas_id, ExternalDBEntity.cas_id)
    mapper.for_member(MetaboliteDBEntity.chemspider_id, ExternalDBEntity.chemspider_id)
    mapper.for_member(MetaboliteDBEntity.metlin_id, ExternalDBEntity.metlin_id)

    mapper.for_member(MetaboliteDBEntity.smiles, ExternalDBEntity.smiles)
    mapper.for_member(MetaboliteDBEntity.inchi, ExternalDBEntity.inchi)
    mapper.for_member(MetaboliteDBEntity.inchikey, ExternalDBEntity.inchikey)
    mapper.for_member(MetaboliteDBEntity.formula, ExternalDBEntity.formula)
    mapper.for_member(MetaboliteDBEntity.charge, ExternalDBEntity.charge)
    mapper.for_member(MetaboliteDBEntity.mass, ExternalDBEntity.mass)
    mapper.for_member(MetaboliteDBEntity.mi_mass, ExternalDBEntity.mi_mass)

    mapper.for_member(MetaboliteDBEntity.attr_mul, ExternalDBEntity.attr_mul)
    mapper.for_member(MetaboliteDBEntity.attr_other, ExternalDBEntity.attr_other)
