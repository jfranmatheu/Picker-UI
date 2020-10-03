from . event import Event
from . condition import Condition


class Trigger:
    def init(self):
        self.event = None
        self.conditions = []
        #self.on_finish = None
        #self.
    
    def set_event(self, event: Event) -> object:
        self.event = event
        return self
    
    def add_condition(self, condition: Condition) -> object:
        self.conditions.append(condition)
        return self
        
    def check(self) -> bool:
        count = 0
        n = len(self.conditions)
        for cond in self.conditions:
            if cond.matched:
                count += 1
        if count == n:
            self.event()
            del self
            return True
        return False
