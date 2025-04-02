from abc import ABC, abstractmethod
from ..builder.File import File

class IGeneratorBase(ABC):
    
    @abstractmethod
    def generate(self, prompt, force_rebuild=False)->File:
        """Generation method"""
