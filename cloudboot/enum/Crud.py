from enum import StrEnum


class Crud(StrEnum):
    CREATE = 'create'
    DELETE = 'delete'
    DESCRIBE = 'describe'
    GET = 'get'
    LIST = 'list'
    UPDATE = 'update'
