import enum
from enum import Enum


@enum.unique
class Source(Enum):
    PROPERTY = 'property'
    FIELD = 'field'
    CONST = 'const'
    FUNCTION = 'function'
