from mfdb_parsinglib.edb_formatting import MultiDict

a = MultiDict({'a': 1})
b = MultiDict({'a': 4})

a.update(b)
print(a)