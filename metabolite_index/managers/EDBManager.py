from eme.data_access import get_repo
from eme.mapper import map_to

from ..apihandlers.ApiClientBase import ApiClientBase
from ..apihandlers.ChebiClient import ChebiClient
from ..apihandlers.KeggClient import KeggClient
from ..apihandlers.PubchemClient import PubchemClient
from ..apihandlers.HMDBClient import HMDBClient
from ..apihandlers.LipidmapsClient import LipidmapsClient

from ..dal import EDBRepository, ExternalDBEntity
from ..edb_formatting import pad_id, depad_id
from ..views.MetaboliteConsistent import MetaboliteConsistent
from ..views.MetaboliteDiscovery import MetaboliteDiscovery


class EDBManager:

    def __init__(self):
        self.apis: dict[str, ApiClientBase] = {
            'chebi': ChebiClient(),
            'kegg': KeggClient(),
            'pubchem': PubchemClient(),
            'hmdb': HMDBClient(),
            'lipidmaps': LipidmapsClient()
        }
        self.repo: EDBRepository = get_repo(ExternalDBEntity)

    def get_metabolite(self, edb_tag: str, edb_id: str, use_cache: bool = True, use_api: bool = True) -> MetaboliteConsistent:
        edb_record: ExternalDBEntity | None = None
        if edb_tag.endswith('_id'):
            edb_tag = edb_tag[:-3]

        if use_cache:
            edb_record = self.repo.get((edb_id, edb_tag))

            if edb_record and edb_record.edb_source != edb_tag:
                # this shouldn't occur ever realistically
                raise Exception(f"!!! WRONG SOURCE QUERIED !!! {edb_record.edb_source} != {edb_tag}")
                # edb_record = self.repo.get_edb(edb_id, edb_tag)

        if not edb_record and use_api:
            # try fetching from API
            print(f"  Fetching {edb_tag} API: {pad_id(edb_id, edb_tag)}")
            edb_api = self.apis[edb_tag].fetch_api(edb_id)

            if edb_api and use_cache:
                # cache record; need to convert to EDB entity for SqlAlchemy
                assert edb_id == edb_api.edb_id and edb_tag == edb_api.edb_source
                edb_record = map_to(edb_api, ExternalDBEntity)
                assert edb_id == edb_record.edb_id and edb_tag == edb_record.edb_source

                self.repo.create(edb_record)
            else:
                # the two classes are interchangeable
                edb_record = edb_api

        return edb_record

    def get_reverse(self, neta: MetaboliteDiscovery, *edb_tags) -> list[MetaboliteConsistent]:
        q = self.repo.select()
        T = ExternalDBEntity# self.repo.T

        for edb_tag in edb_tags:
            search_val = getattr(neta, edb_tag)

            # if not search_val:
            #     # skip where clause if there's no value to reverse query by
            #     continue
            #search_val =

            if isinstance(search_val, (set, list, tuple)):
                # SQL IN
                search_val = set(map(lambda x: depad_id(x, edb_tag), search_val))
                q = q.filter(getattr(T, edb_tag).in_(search_val))
            else:
                # scalar WHERE
                search_val = depad_id(search_val, edb_tag)
                q = q.filter(getattr(T, edb_tag) == search_val)
            return q.all()

    def resolve_secondary_id(self, edb_tag: str, edb_id: str) -> str | None:

        # not implemented
        return None
