from dataclasses import dataclass
from abc import ABC, abstractmethod
from io import IOBase
from PIL import Image
from io import BytesIO, StringIO

@dataclass
class File:
    ext: str
    file: IOBase

    def get_file(self):
        self.file.seek(0)
        return self.file
    
class IGeneratorBase(ABC):    
    @abstractmethod
    def generate(self, prompt, force_rebuild=False)->File:
        """Generation method"""

    @abstractmethod
    def ext()->str:
        """Content file extension"""
    
class TextGenerator(IGeneratorBase):
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    def generate(self, prompt, **_):
        return File(self.ext(), StringIO(prompt))
    
    def ext(self):
        return 'txt'

class ImageGenerator(IGeneratorBase):
    def __init__(self):
        pass

    def generate(self, *_, **__):
        stream = BytesIO()
        Image.new(mode='RGBA', size=(1,1), color=1).save(stream)
        return File(self.ext(), stream)
    
    def ext(self):
        return 'png'