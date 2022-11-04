from eme.data_access import Repository, RepositoryBase
from sqlalchemy import and_, func

from ..entities.ExternalDBEntity import ExternalDBEntity


@Repository(ExternalDBEntity)
class EDBRepository(RepositoryBase):
    # def get_edb(self, edb_id, edb_tag) -> ExternalDBEntity:
    #     return self.session.query(ExternalDBEntity)\
    #     .filter(ExternalDBEntity.edb_id == edb_id)\
    #     .filter(ExternalDBEntity.edb_source == edb_tag)\
    #     .first()

    pass