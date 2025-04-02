from dataclasses import dataclass
from ..builder.File import File
from io import IOBase
from ..preprocessor.text.IdentityProcessor import IdentityProcessor

@dataclass
class Post:
    message: File
    media: File

    def get_real_message(self, processor=IdentityProcessor())->str:
        if self.message:
            self.message.file.seek(0)
            return processor.process(self.message.file.read())
        return None
    
    def get_real_media(self)->IOBase:
        if self.media:
            self.media.file.seek(0)
            return self.media.file
        return None
    
    ext2ct = {
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'txt': 'text/plain'
    }

    def get_content_type(self):
        if self.media and self.media.ext in Post.ext2ct:
            return Post.ext2ct[self.media.ext]
        return 'application/octet-stream'