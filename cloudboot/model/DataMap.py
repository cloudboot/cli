from InquirerPy.base import Choice

from cloudboot.model.Base import Base


class DataMap(Base):
    keys = []
    map = {}

    def push(self, key, value):
        key.apped(key)
        map[key] = value

    def choices(self):
        elements = []
        for key in self.keys:
            elements.append(Choice(name=key, value=self.map[key]))
        return elements
