from __future__ import annotations 
import simple_blogger.builder.content
from abc import ABC, abstractmethod

class IPromptBuilder(ABC):
    @abstractmethod
    def build(self, force_rebuild=False, *_, **__)->str:
        """ Prompt builder method """

class IdentityPromptBuilder(IPromptBuilder):
    def __init__(self, prompt:str):
        self.prompt = prompt
    
    def build(self, *_, **__):
        return self.prompt
    
class TaskPromptBuilder(IPromptBuilder):
    def __init__(self, task_builder, prompt_constructor):
       self.task_builder=task_builder
       self.prompt_constructor=prompt_constructor

    def build(self, *_, **__):
        task = self.task_builder.build()
        return task and self.prompt_constructor(task=task) 

class ContentBuilderPromptBuilder(IPromptBuilder):
    def __init__(self, content_builder: simple_blogger.builder.content.IContentBuilder):
        self.content_builder=content_builder
    
    def build(self, force_rebuild=False):
        return content:=self.content_builder.build(force_rebuild=force_rebuild) and content.get_file().read()