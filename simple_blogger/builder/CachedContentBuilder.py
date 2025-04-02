from ..cache.FileCache import FileCache
from .IContentBuilder import IContentBuilder
from .File import File

class CachedBuilder(IContentBuilder):
    def __init__(self, path, builder, cache=None, filename='topic', extension = 'txt'):
        self.path = path
        self.builder = builder
        self.cache = cache or FileCache(is_binary = extension != 'txt')
        self.filename = filename
        self.extension = extension

    def build(self, prompt=None, force_rebuild=False):
        uri = f"{self.path}/{self.filename}.{self.extension}"
        if force_rebuild or (cached := self.cache.load(uri=uri)) is None:
            new = self.builder.build(prompt=prompt)
            if new is not None:
                self.cache.save(uri=uri, io_base=new.file)
            return new
        return File(self.extension, cached)