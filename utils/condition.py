from enum import Enum


class ConditionalOperator(Enum):
    LESS = 0,
    GREATER = 1,
    EQUAL = 2,
    NOT_EQUAL = 3,
    LESS_EQUAL = 4,
    GREATER_EQUAL = 5


class Condition:
    def __init__(self, data, attr: str, target, operation: ConditionalOperator):
        self.data = data
        self.attr = attr
        # self.current_value = getattr(data, attr)
        self.target_value = target
        self.op = operation
        self.__matched = False
    
    @property
    def matched(self):
        if not self.__matched:
            self.__matched = self.match()
        return self.__matched
        
    def match(self) -> bool:
        if self.op == ConditionalOperator.EQUAL:
            return self.target_value == getattr(self.data, self.attr)
        elif self.op == ConditionalOperator.NOT_EQUAL:
            return self.target_value != getattr(self.data, self.attr)
        elif self.op == ConditionalOperator.LESS:
            return self.target_value < getattr(self.data, self.attr)
        elif self.op == ConditionalOperator.GREATER:
            return self.target_value > getattr(self.data, self.attr)
        elif self.op == ConditionalOperator.LESS_EQUAL:
            return self.target_value <= getattr(self.data, self.attr)
        elif self.op == ConditionalOperator.GREATER_EQUAL:
            return self.target_value >= getattr(self.data, self.attr)
        return True
    