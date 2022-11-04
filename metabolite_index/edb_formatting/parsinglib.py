from itertools import chain

def rlen(v):
    if isinstance(v, list):
        return len(v)
    elif v is None:
        return 0
    else:
        return 1


def _nil(var):
    if not bool(var):
        return True
    # accounts for xml newlines, whitespace & etc
    s = var.strip().replace('\r', '').replace('\n', '')
    return not bool(s)


def strip_attr(r, key, prefix):
    if key not in r or not r[key]:
        return

    if isinstance(r[key], list):
        r[key] = list(map(lambda v: v.lstrip(prefix), r[key]))
    else:
        r[key] = r[key].lstrip(prefix)



def flatten(v: dict, attr):
    if attr in v and isinstance(v[attr], (list, tuple, set)):
        v[attr] = try_flatten(v[attr])


def try_flatten(arr: list):
    """
    Flattens collections within dict if their lengths = 1
    :param v: dict
    :param attr: attribute to flatten
    :return:
    """

    if isinstance(arr, (list, tuple, set)):
        assert len(arr) <= 1, "can't flatten list"
        return next(chain(arr), None)
    # scalar
    return arr



def force_flatten(arr, store_in: list):
    """
    Flattens collections regardless of size
    :param coll: collection to flatten
    :param store_in: extra container to store stripped attributes in
    :return:
    """
    if isinstance(arr, (list, tuple, set)):
        if len(arr) > 1:
            store_in.append(list(arr)[1:])
            return arr[0]

        return next(chain(arr), None)
    # scalar
    return arr


def force_list(r, key, f=None):
    """
    Forces value to be a list of element 1
    """
    if key not in r:
        return

    v = r[key]

    if isinstance(v, (list, tuple, set)):
        if f is not None:
            r[key] = [f(e) for e in v]
        else:
            r[key] = v
    elif v is None:
        r[key] = None
    else:
        if f is not None:
            r[key] = [f(v)]
        else:
            r[key] = [v]

def remap_keys(v, _mapping: dict):
    for k in set(v) & set(_mapping):
        new_key = _mapping[k]
        val = v.pop(k)

        if new_key not in v:
            # best effort to keep things scalar
            v[new_key] = val
        else:
            # if multiple values found, extend it to be a list
            if not isinstance(v[new_key], list):
                v[new_key] = [v[new_key]]

            if isinstance(val, list):
                v[new_key].extend(val)
            else:
                v[new_key].append(val)

def handle_quotes(me, k):
    """
    Replaces problematic characters for json serialization
    "
    :param me:
    :param k:
    :return:
    """
    if k in me:
        if isinstance(me[k], list):
            me[k] = list(map(lambda x: x.replace('"', '”').replace('\t', ' '), me[k]))
        else:
            me[k] = me[k].replace('"', '”').replace('\t', ' ')


class MultiDict(dict):
    """
    A dict-like object that tries to keep added items singular
    """

    def append(self, key, value):
        if oldval := self.get(key):
            # there are multiple entries in buffer, store them in a list
            if not isinstance(oldval, list):
                oldval = [oldval]
                self.__setitem__(key, oldval)
            oldval.append(value)
        else:
            self.__setitem__(key, value)
