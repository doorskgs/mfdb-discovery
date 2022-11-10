from operator import itemgetter

from metabolite_index.edb_formatting.cluster1d import cluster1d_eps, cluster1d_fixed, get_float_precision


class MultiDict(dict):
    """
    A dict-like object that tries to keep added items scalar
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

    def extend(self, key, value: list):
        if isinstance(value, (list, tuple, set)):
            for val in value:
                self.append(key, val)
        else:
            self.append(key, value)


class TrimSet(set):
    def __init__(self, seq=(), trimmer=None):
        super().__init__(seq)

        self.trimmer = trimmer

    def add(self, val):
        if val is not None:
            if self.trimmer:
                val = self.trimmer(val)
            super().add(val)

    def update(self, _set):
        if self.trimmer:
            _updated_set = set(self.trimmer(x) for x in _set if x is not None)
        else:
            _updated_set = set(x for x in _set if x is not None)

        if _updated_set:
            super().update(_updated_set)

    def __repr__(self):
        return repr_trimset(self)

class AlmostEqualSet(set):
    def __init__(self, seq=(), eps=0.0005):
        super().__init__(seq)
        self.eps = eps

    def get_set(self):
        # cluster floats
        clusters = cluster1d_fixed(self)
        cluster_reprs = []

        for cluster in clusters:
            # get the float with the highest precision to represent the cluster:
            prec = [(f,get_float_precision(f)) for f in cluster]
            rf = max(prec, key=itemgetter(1))[0]
            cluster_reprs.append(rf)

        return set(cluster_reprs)

    def __repr__(self):
        return repr(self.get_set())


def repr_trimset(s: set | TrimSet):
    if hasattr(s, 'trimmer') and s.trimmer:
        trimmer = lambda x: s.trimmer(str(x))
    else:
        trimmer = str
    return ' • '.join(map(trimmer, s))
