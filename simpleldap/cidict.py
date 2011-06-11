"""
A re-implementation of the ldap module's cidict that inherits from dict instead
of UserDict so that we can, in turn, inherit from cidict.
"""


class cidict(dict):
    """
    Case-insensitive but case-respecting dictionary.
    """

    def __init__(self, default=None):
        self._keys = {}
        super(cidict, self).__init__({})
        self.update(default or {})

    def __getitem__(self, key):
        return super(cidict, self).__getitem__(key.lower())

    def __setitem__(self, key, value):
        lower_key = key.lower()
        self._keys[lower_key] = key
        super(cidict, self).__setitem__(lower_key, value)

    def __delitem__(self, key):
        lower_key = key.lower()
        del self._keys[lower_key]
        super(cidict, self).__delitem__(lower_key)

    def update(self, dict):
        for key in dict:
            self[key] = dict[key]

    def has_key(self, key):
        return super(cidict, self).has_key(key.lower())

    __contains__ = has_key

    def get(self, key, *args, **kwargs):
        return super(cidict, self).get(key.lower(), *args, **kwargs)

    def keys(self):
        return self._keys.values()

    def items(self):
        return [(k, self[k]) for k in self.keys()]
