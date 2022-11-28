from mfdb_parsinglib.edb_formatting.padding import get_id_from_url
from mfdb_parsinglib.edb_formatting.structs import MultiDict


def parse_pubchem(edb_id, content, cont_refs, _mapping):
    """
    Parses API response for PubChem

    :param edb_id:
    :param c0:
    :param c1:
    :return:
    """

    data = MultiDict()

    # parse xrefs:
    _links = cont_refs['InformationList']['Information'][0]['SBURL']

    # guess xref IDs
    for link in _links:
        link = link.lower()

        db_id, api_db_tag = get_id_from_url(link)

        if db_id is None:
            # unrecognized XREF
            continue
        data.append(api_db_tag+'_id', db_id)


    _resp = content['PC_Compounds'][0]
    props = _resp.pop('props')
    data.append('pubchem_id',  _resp['id']['id']['cid'])

    hat_geci = []

    for prop in props:
        label = prop['urn']['label']

        attr, valt = _mapping.get(label, (label, 'sval'))
        attr = attr.lower()

        if isinstance(prop['value'], dict):
            value = prop['value'].get(valt)

            if value is not None:
                data.append(attr, value)
            else:
                # skip attr as it's not mapped
                hat_geci.append((attr, valt, prop['value']))
        else:
            data.append(attr, prop['value'])

    # merge and transform to standard json
    return dict(data)
