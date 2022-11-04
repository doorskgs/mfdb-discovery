from collections import defaultdict

from metabolite_index.edb_formatting import MultiDict


def parse_kegg(edb_id, content):
    """
    https://www.kegg.jp/kegg/docs/dbentry.html

    :param edb_id:
    :param content:
    :return:
    """

    content = content.split('\n')
    data = MultiDict()
    _refs = MultiDict()
    handle = iter(content)
    kegg_id = edb_id

    # smart guess whitespace from 1st line
    line = next(handle)
    try:
        FL = line.index(edb_id.upper())
    except:
        return None

    state = None
    for line in handle:
        if line.startswith('///') or line == '':
            # /// skips idk
            continue

        if not line.startswith("   "):
            # interpret labels as regular lines, but save the label
            state = line.split()[0]
            line = line[FL:].rstrip('\n')
        else:
            line = line.lstrip().rstrip('\n')

        if 'ENTRY' == state:
            kegg_id = line
        elif 'DBLINKS' == state:
            # foreign references:
            db_tag, ref_ids = line.split(': ')

            if db_tag.endswith('_id'):
                db_tag = db_tag[:-3]
            db_tag = db_tag.lower()

            for edb_id in ref_ids.split(" "):
                _refs.append(db_tag, edb_id)
        else:
            data.append(state.lower(), line)

    # todo: parse rest of file ?

    # merge and transform to standard json
    return {'kegg_id': kegg_id, **data, **_refs}
