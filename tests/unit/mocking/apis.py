import json
import os
from metabolite_index.edb_formatting import get_id_from_url


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def json(self):
            return json.loads(self.content)

        @property
        def content(self):
            return self.text.encode('utf8')

    uri = args[0] if len(args) >= 1 else kwargs['url']
    db_id, db_tag = get_id_from_url(uri)

    if 'hmdb' == db_tag:
        fn = f'data/apis/{db_id}.xml'
    elif 'chebi' == db_tag:
        fn = 'data/apis/getCompleteEntity.xml'
    elif 'kegg' == db_tag:
        fn = f'data/apis/cpd_{db_id}.txt'
    else:
        raise NotImplementedError("test")
        #return MockResponse(None, 404)

    if not os.path.exists(fn):
        return MockResponse(None, 404)
    with open(fn, 'r') as fh:
        data = fh.read()
    return MockResponse(data, 200)

