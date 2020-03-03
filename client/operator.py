import enum
from enum import Enum


@enum.unique
class Operator(Enum):
    EQUAL = '='
    GRATER = '>'
    GRATER_EQUAL = '>='
    IN = 'in'
    NOT_IN = 'not in'
    IS = 'is'
    IS_NOT = 'is not'
    LESS = '<'
    LESS_EQUAL = '<='
    LIKE = 'like'
    NOT_EQUAL = '<>'
    NOT_LIKE = 'not like'
