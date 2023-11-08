from cloudboot.model.Base import Base


class Project(Base):
    project_id = ''
    name = ''
    project_number = ''

    def __init__(self, raw_data: str):
        data = raw_data.split()
        if len(data):
            self.project_id = data[0]
            self.name = data[1]
            self.project_number = data[2]
