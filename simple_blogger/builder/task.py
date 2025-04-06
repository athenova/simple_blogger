from abc import ABC, abstractmethod

class ITaskBuilder(ABC):
    @abstractmethod
    def build(self):
        """Task extractor method """

class TaskExtractor(ITaskBuilder):
    def __init__(self, tasks, check):
        self.tasks = tasks
        self.check = check

    def build(self):
        for task in self.tasks:
            if self.check(task=task, tasks=self.tasks):
                return task
        return None