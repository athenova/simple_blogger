from __future__ import annotations 
import simple_blogger.builder.prompt
from simple_blogger.generator import File
from simple_blogger.cache.file_system import FileCache
from simple_blogger.builder.task import ITaskBuilder
from abc import ABC, abstractmethod

class IContentBuilder(ABC):    
    @abstractmethod
    def build(self, force_rebuild=False)->File:
        """Content builder method"""

    @abstractmethod
    def ext(self)->str:
        """Content extension"""

class ContentBuilder(IContentBuilder):
    def __init__(self, generator, prompt_builder:simple_blogger.builder.prompt.IPromptBuilder):
        self.generator = generator
        self.prompt_builder = prompt_builder

    def build(self, force_rebuild=False):
        prompt = self.prompt_builder.build(force_rebuild=force_rebuild)
        return prompt and self.generator.generate(prompt, force_rebuild=force_rebuild)
    
    def ext(self):
        return self.generator.ext()

class CachedContentBuilder(IContentBuilder):
    def __init__(self, task_builder:ITaskBuilder, path_constructor, builder:IContentBuilder, cache=None, filename='topic'):
        self.task_builder = task_builder
        self.path_constructor = path_constructor
        self.builder = builder
        self.cache = cache or FileCache(is_binary = builder.ext() != 'txt')
        self.filename = filename

    def __build(self, task, force_rebuild):
        uri = f"{self.path_constructor(task)}/{self.filename}.{self.builder.ext()}"
        if force_rebuild or (cached := self.cache.load(uri=uri)) is None:
            new = self.builder.build(force_rebuild=force_rebuild)
            if new is not None:
                self.cache.save(uri=uri, io_base=new.file)
            return new
        return File(self.builder.ext(), cached) 

    def build(self, force_rebuild=False, **__):
        task = self.task_builder.build()
        return task and self.__build(task, force_rebuild)
    
    def ext(self):
        return self.builder.ext()