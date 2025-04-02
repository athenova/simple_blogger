from abc import ABC, abstractmethod
from .File import File

class IContentBuilder(ABC):
    
    @abstractmethod
    def build(self, prompt=None, force_rebuild=False)->File:
        """Content builder method"""