class Base(object):

    def _get_value(self, item):
        return getattr(self, item)

    def __iter__(self):
        attributes = dir(self)
        for attribute in attributes:
            if not attribute.startswith('_'):
                value = self._get_value(attribute)
                if value and not isinstance(value, (int, str, bool, float)):
                    value = dict(value)
                yield attribute, value
