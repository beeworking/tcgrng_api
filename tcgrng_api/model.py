class Model(object):
    _models = {}
    _collection = None

    def __init__(self, **kwargs):
        self._keys = []

        for key in kwargs:
            self._keys.append(key)
            if key in self._models:
                setattr(self, key, self._models[key](**kwargs[key]))
            else:
                setattr(self, key, kwargs[key])

    def json(self):
        json = {}

        for key in self._keys:
            if isinstance(key, Model):
                json[key] = getattr(self, key).json()
            else:
                json[key] = getattr(self, key)

        return json
