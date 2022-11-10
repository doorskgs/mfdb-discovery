from typing import Generator, Iterable

from eme.data_access import Repository, RepositoryBase
from sqlalchemy import and_, func, select, text

from ..ctx import get_engine
from ..entities.ExternalDBEntity import ExternalDBEntity


@Repository(ExternalDBEntity)
class EDBRepository(RepositoryBase):

    def list_chebi_iter(self, stop_at=None) -> Iterable[ExternalDBEntity]:
        q = self.session.query(self.T)\
            .filter(ExternalDBEntity.edb_source == 'chebi')

        if stop_at:
            q = q.limit(stop_at)

        return q.yield_per(1000)
