from __future__ import annotations 
import simple_blogger.builder.content
from abc import ABC, abstractmethod

class IPromptBuilder(ABC):
    @abstractmethod
    def build(self, force_rebuild=False)->str:
        """ Prompt builder method """

class IdentityPromptBuilder(IPromptBuilder):
    def __init__(self, prompt:str):
        self.prompt = prompt
    
    def build(self, *_, **__):
        return self.prompt
    
class TaskPromptBuilder(IPromptBuilder):
    def __init__(self, tasks:list, check, prompt_builder):
        self.tasks=tasks
        self.check=check
        self.prompt_builder=prompt_builder

    def build(self, *_, **__):
        for task in self.tasks:
            if self.check(task):
                return self.prompt_builder(task)
        return None

class ContentBuilderPromptBuilder(IPromptBuilder):
    def __init__(self, content_builder: simple_blogger.builder.content.IContentBuilder):
        self.content_builder = content_builder
    
    def build(self, force_rebuild=False):
        return self.content_builder.build(force_rebuild=force_rebuild).get_file().read()