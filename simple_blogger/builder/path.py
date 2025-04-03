from abc import ABC, abstractmethod

class IPathBuilder(ABC):
    @abstractmethod
    def build()->str:
        """ Path builder method """

class IdentityPathBuilder(IPathBuilder):
    def __init__(self, path:str):
        self.path = path
    
    def build(self):
        return self.path
    
class TaskPathBuilder(IPathBuilder):
    def __init__(self, tasks:list, check, path_builder):
        self.tasks=tasks
        self.check=check
        self.path_builder=path_builder

    def build(self):
        for task in self.tasks:
            if self.check(task):
                return self.path_builder(task)
        return None