from typing import Iterable


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
