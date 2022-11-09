from eme.data_access import Repository, RepositoryBase
from sqlalchemy import and_, func

from ..entities.ExternalDBEntity import ExternalDBEntity


@Repository(ExternalDBEntity)
class EDBRepository(RepositoryBase):
    pass
