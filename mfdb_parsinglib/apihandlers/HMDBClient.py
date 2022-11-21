import requests

from io import StringIO, BytesIO
import xml.etree.ElementTree as ET

from lxml import etree

from .ApiClientBase import ApiClientBase
from ..edb_formatting import pad_id, preprocess, remap_keys, map_to_edb_format, replace_obvious_hmdb_id, MultiDict
from ..dal import ExternalDBEntity


class HMDBClient(ApiClientBase):
    _reverse = (
        'pubchem_id', 'kegg_id', 'chebi_id',
    )

    explore_children = {'secondary_accessions','synonyms'}


    def __init__(self):
        super().__init__()

        self.load_mapping('hmdb')

    def fetch_api(self, edb_id):
        db_id = pad_id(edb_id, 'hmdb_id')
        r = requests.get(url=f'https://hmdb.ca/metabolites/{db_id}.xml', allow_redirects=False)

        if r.is_redirect or r.status_code == 301:
            # we queried a secondary ID, follow the redirect of the api
            next_url = r.next.url+'.xml'
            print("  HMDB: redirecting to", next_url)
            r = requests.get(url=next_url)

        is_xml = r.headers['content-type'].startswith('application/xml')
        if r.status_code != 200 and r.status_code != 304 or r.content is None or not is_xml:
            return None

        #xmlns = 'http://www.hmdb.ca'
        #filter_tag = f'{{{xmlns}}}metabolite'
        filter_tag = 'metabolite'

        context = etree.iterparse(BytesIO(r.content), events=('end',), tag=filter_tag)
        context = iter(context)
        _xevt, xmeta = next(context)

        data = MultiDict()

        # parse lxml's hierarchy into a dictionary
        for tag in xmeta:
            tag_name = tag.tag#.removeprefix('{' + xmlns + '}')

            if len(tag) == 0:
                data.append(tag_name, tag.text)
            else:
                if tag_name in self.explore_children:
                    for child in tag:
                        # assert len(child) == 0
                        data.append(tag_name, child.text)
        xmeta.clear(keep_tail=False)

        remap_keys(data, self._mapping)
        preprocess(data)
        data, etc = map_to_edb_format(data, important_attr=self._important_attr)

        data['edb_source'] = 'hmdb'
        return ExternalDBEntity(**data)
