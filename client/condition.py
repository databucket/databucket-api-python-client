from client.source import Source
from client.operator import Operator


class Condition:
    left_source = None
    left_value = None
    operator = None
    right_source = None
    right_value = None

    def __init__(self, *, left_source: Source, left_value, operator: Operator, right_source: Source, right_value):
        self.left_source = left_source.value
        if left_source == Source.PROPERTY:
            self.left_value = f'$.{left_value}'
        else:
            self.left_value = left_value
        self.operator = operator
        self.right_source = right_source.value
        if right_source == Source.PROPERTY:
            self.right_value = f'$.{right_value}'
        else:
            self.right_value = right_value

