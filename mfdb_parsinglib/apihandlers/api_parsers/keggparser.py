import re
from collections import defaultdict

from mfdb_parsinglib.edb_formatting import MultiDict


KEGG_END = '///'
KEGG_START = "ENTRY"
KEGG_LINE_PATTERN = re.compile(r'[a-zA-Z0-9_]*(\s*)([a-zA-Z0-9_]*)')
to_float = {'exact_mass', 'mol_weight', 'charge'}


def parse_kegg(stream):
    """
    https://www.kegg.jp/kegg/docs/dbentry.html

    :param content:
    :return:
    """
    FL = 0

    data = MultiDict()
    state = None

    for line in stream:
        if line == '' or line == '\n':
            continue
        elif line.startswith(KEGG_END):
            # kegg entry ended, save and yield
            yield data

            # start new entry
            data = MultiDict()
            state = None
            continue
        elif line.startswith(KEGG_START) and FL == 0:
            # first line - determine prefix length of KEGG's format
            groups = re.match(KEGG_LINE_PATTERN, line)
            FL = len(groups[1])+len(KEGG_START)

        values = line.split()

        if not line.startswith("   "):
            # interpret new attribute labels as regular lines, but save the label state for the next lines
            state = values[0].lower()
            values = values[1:]

        if 'dblinks' == state or 'DBLINKS' == state:
            # foreign reference - split by spaces
            db_source = values[0].rstrip(':').removesuffix('_id').lower()
            data.extend(db_source, values[1:])

        else:
            # any other attribute
            if state in to_float and line:
                values = list(map(float, values))
            elif 'name' == state:
                values = set(line[FL:].strip().split(';'))
                if '' in values:
                    values.remove('')
            elif state == 'entry':
                values = values[0]

            data.extend(state.lower(), values)
