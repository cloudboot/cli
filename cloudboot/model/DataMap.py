from InquirerPy.base import Choice

from cloudboot.model.Base import Base


class DataMap(Base):
    keys = []
    map = {}

    def choices(self):
        elements = []
        for key in self.keys:
            elements.append(Choice(name=key, value=self.map[key]))
        return elements
