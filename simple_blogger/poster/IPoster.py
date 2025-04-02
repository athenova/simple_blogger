from abc import ABC, abstractmethod
from .Post import Post

class IPoster(ABC):
    @abstractmethod
    def post(self, post:Post, **_):
        """ Post method """