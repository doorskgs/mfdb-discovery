from eme.data_access import get_repo
from eme.mapper import map_to

from ..DiscoveryOptions import DiscoveryOptions
from ..apihandlers.ApiClientBase import ApiClientBase
from ..apihandlers.ChebiClient import ChebiClient
from ..apihandlers.KeggClient import KeggClient
from ..apihandlers.PubchemClient import PubchemClient
from ..apihandlers.HMDBClient import HMDBClient
from ..apihandlers.LipidmapsClient import LipidmapsClient

from ..dal import EDBRepository, SecondaryIDRepository, ExternalDBEntity, SecondaryID
from ..edb_formatting import pad_id, depad_id
from ..views.MetaboliteConsistent import MetaboliteConsistent
from ..views.MetaboliteDiscovery import MetaboliteDiscovery


class EDBManager:

    def __init__(self, secondary_ids: set, opts):
        """
        Manages External DB's in-app cache and EDB's public API to fetch EDB records
        :param secondary_ids:
        """
        self.apis: dict[str, ApiClientBase] = {
            'chebi': ChebiClient(),
            'kegg': KeggClient(),
            'pubchem': PubchemClient(),
            'hmdb': HMDBClient(),
            'lipidmaps': LipidmapsClient()
        }

        self.repo: EDBRepository = get_repo(ExternalDBEntity)
        self.repo2nd: SecondaryIDRepository = get_repo(SecondaryID)

        self.secondary_ids = secondary_ids
        self.opts = opts

    def get_metabolite(self, edb_tag: str, edb_id: str) -> MetaboliteConsistent:
        """

        :param edb_tag:
        :param edb_id:
        :return:
        """
        edb_record: MetaboliteConsistent | None = None

        edb_source = edb_tag[:-3] if edb_tag.endswith('_id') else edb_tag
        opts = self.opts.get_opts(edb_source)

        if opts.cache_enabled:
            # find by edb table
            edb_record = self.repo.get((edb_id, edb_source))

        if not edb_record:
            # find primary ID from secondary id
            if edb_id := self.resolve_secondary_id(edb_source, edb_id):
                # query again
                edb_record = self.repo.get((edb_id, edb_source))

        if not edb_record and opts.api_enabled:
            edb_record = self.fetch_api(edb_source, edb_id, save_in_cache=opts.cache_upsert)

        return edb_record

    def get_reverse(self, meta: MetaboliteDiscovery, *edb_tags) -> list[MetaboliteConsistent]:
        """

        :param meta:
        :param edb_tags:
        :return:
        """
        q = self.repo.session.query(ExternalDBEntity)

        for edb_tag in edb_tags:
            search_val = getattr(meta, edb_tag)
            _column = getattr(ExternalDBEntity, edb_tag)

            if isinstance(search_val, (set, list, tuple)):
                # SQL IN
                search_val = set(map(lambda x: depad_id(x, edb_tag), search_val))
                q = q.filter(_column.in_(search_val))
            else:
                # scalar WHERE
                search_val = depad_id(search_val, edb_tag)
                q = q.filter(_column == search_val)
            return q.all()

    def fetch_api(self, edb_tag, edb_id, save_in_cache=False):
        """
        fetch edb record from their public API
        :param edb_tag:
        :param edb_id:
        :param save_in_cache:
        :return:
        """

        edb_id_padded = pad_id(edb_id, edb_tag)
        print(f"  Fetching {edb_tag} API: {edb_id_padded}")
        edb_api = self.apis[edb_tag].fetch_api(edb_id_padded)

        if edb_api and save_in_cache:
            # save api results to table
            # cache record; need to convert to EDB entity for SqlAlchemy
            assert edb_id == edb_api.edb_id and edb_tag == edb_api.edb_source
            edb_record = map_to(edb_api, ExternalDBEntity)
            assert edb_id == edb_record.edb_id and edb_tag == edb_record.edb_source

            self.repo.create(edb_record)
        else:
            # the two classes are interchangeable
            edb_record = edb_api

        return edb_record

    def resolve_secondary_id(self, edb_source, edb_id):
        """
        Gets record by querying EDB ID as a secondary ID instead of pkey
        :param edb_source:
        :param edb_id:
        :return:
        """
        resp = self.repo2nd.get_primary_id(edb_id, edb_source)

        if not resp:
            return edb_id
        else:
            edb_tag = edb_source + '_id'
            self.secondary_ids.add((edb_tag, edb_id))

            return resp.edb_id
