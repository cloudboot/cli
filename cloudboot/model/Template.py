from cloudboot.model.Base import Base


class Template(Base):
    name: str
    src: str
    entrypoint: str = 'main'

    def __init__(self, name, src, entrypoint):
        self.name = name
        self.src = src
        self.entrypoint = entrypoint
