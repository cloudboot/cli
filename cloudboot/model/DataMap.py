from InquirerPy.base import Choice

from cloudboot.model.Base import Base


class DataMap(Base):
    key = 'name'
    display_name = 'displayName'
    keys = []
    map = {}

    def __init__(self, key, display_name):
        self.key = key
        self.display_name = display_name
        self.keys = []
        self.map = {}

    def push_one(self, key, value):
        self.keys.append(key)
        self.map[key] = value

    def is_empty(self):
        return not len(self.keys) or not len(self.map)

    def push_all(self, items: list):
        for item in items:
            _key = item[self.key]
            self.keys.append(_key)
            self.map[_key] = item

    def choices(self):
        elements = []
        for _key in self.keys:
            elements.append(Choice(name=f'{_key} - {self.map[_key][self.display_name]}', value=self.map[_key]))
        return elements

    def find_choice(self, name, _choices=None):
        if not _choices:
            _choices = self.choices()
        for choice in _choices:
            if name == choice.name:
                return choice.value
        return None
