from simple_blogger.generator import File
from simple_blogger.preprocessor.text import IdentityProcessor
from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import IOBase

@dataclass
class Post:
    message: File
    media: File

    def get_real_message(self, processor=IdentityProcessor())->str:
        if self.message:
            return processor.process(self.message.get_file().read())
        return None
    
    def get_real_media(self)->IOBase:
        if self.media:
            return self.media.get_file()
        return None
    
    ext2ct = {
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'txt': 'text/plain'
    }

    def get_content_type(self)->str:
        if self.media and self.media.ext in Post.ext2ct:
            return Post.ext2ct[self.media.ext]
        return 'application/octet-stream'
    
class IPoster(ABC):
    @abstractmethod
    def post(self, post:Post, **_):
        """ Post method """
